title: Type-safe vector addition with Dependent Types
date: 2014-12-03 08:30
author: Chris Stucchio
tags: scala, breeze, dependent types, vector spaces
category: scala
nolinkback: true

The two sides of my programming world have long suffered a disconnect. When I build a robust low latency system, I typically write it in a language like Scala. I make great use of type safety to reduce the number of errors I've made. On the other hand, when I need to do some harcore number crunching, I always go back to Python (and lately sometimes Julia). Unfortunately for me, most of the people hacking on type systems are not focusing their attention on the problems that data geeks run into regularly.

This post illustrates how to use the type system to detect one particular problem I've run into - incorrectly mixing different vector representations. One possible problem:

```scala
val v3 = DenseVector.zeros[Double](3)
val v4 = DenseVector.zeros[Double](4)
v3 + v4 //RUNTIME ERROR - Vectors must have same dimension
```

This isn't a big problem. The minute I run my code I'll discover the error - [Breeze](https://github.com/scalanlp/breeze) has a lot of [runtime checks](https://github.com/scalanlp/breeze/blob/master/math/src/main/scala/breeze/linalg/DenseVector.scala#L257) with informative error messages.

Here is a more subtle error:
```scala
val securityReturns = DenseVector.zeros[Double](numSecurities)
val pcaRepresentation = DenseVector.zeros[Double](numSecurities)
// do some work
val tmp = pcaRepresentation
val result = securityReturns + tmp
```

See the problem here? No runtime error was raised and my code returns *an answer*. The problem is that the answer is deeply wrong - I've added together two vectors from different vector spaces that happen to have the same dimension. The number `securityReturns(0)` represents the daily return of the stock symbol AAA. The number `pcaRepresentation(0)` represents the largest contribution to the variance of the returns, and is a weighted sum of the returns of a large number of securities. **The sum of these two is meaningless!**

# Dependent Types

Most programming languages have functions from values to values. E.g., in Javascript:

```javascript
val f = function(x) { return x*x; }
```

Most modern languages with type systems (a notable exception being Go) also have functions from *types* to *values*:
```java
List<Foo> list = new ArrayList<Foo>()
```
In essence, generic types allow functions mapping a type (in this case `Foo`) to a value (a specific `ArrayList<Foo>`).

[Dependent types](http://en.wikipedia.org/wiki/Dependent_type) are the reverse - a function from *values* to *types*. What I'd like to do is construct a *value* representing a specific vector space and get back a *type* representing vectors in that vector space. I can then insist that vector addition take vectors of the same type - i.e., vectors from different vector spaces cannot be added (even if they have the same dimension).

# Dependently typed vectors

To begin, I build a wrapper around Breeze's vector space:

```scala
trait RealVectorSpace {
  val dim: Int
  def zero: V

  case class V(u: DenseVector[Double])  {
    implicit def +(w: V) = V(u+w.u)
    implicit def *(a: Double) = V(u*a)
  }
}
```

Then I define the obvious implementation:

```scala
case class R(val dim: Int) extends RealVectorSpace {
  def zero = V(DenseVector.zeros[Double](dim))
}
```

The important point here is that each vector is explicitly a member of one particular vector space. Now the following code works:

```scala
val R3 = R(3)
val x = R3.zero
val y = R3.zero
//Some code modifying x, y
x + y
```

This compiles with no problem. But this doesn't:

```scala
val R4 = R(4)
val z = R4.zero
x + z
```

The result:
```
[info] Compiling 1 Scala source to /home/stucchio/src/vector_space_dependent_type/target/scala-2.11/classes...
[error] /home/stucchio/src/vector_space_dependent_type/src/main/scala/vector_space/package.scala:27: type mismatch;
[error]  found   : com.chrisstucchio.vectorspace.package.R4.V
[error]  required: com.chrisstucchio.vectorspace.package.R3.V
```

It's not allowed to add vectors from different vector spaces. What about with the same dimension?

```scala
val securityRepresentation = R(numSecurities)
val pcaRepresentation = R(numSecurities)

val securityReturns = securityRepresentation.zero
//...
val pcaReturns = pcaRepresentation.zero
//...
securityReturns + pcaReturns
```
Result:
```
[error] /home/stucchio/src/vector_space_dependent_type/src/main/scala/vector_space/package.scala:27: type mismatch;
[error]  found   : com.chrisstucchio.vectorspace.package.securityRepresentation.V
[error]  required: com.chrisstucchio.vectorspace.package.pcaRepresentation.V
```

Even though the dimension is the same, I am not allowed to mix representations.

## Obvious extensions

It would be reasonably straightforward to define multiple types of vector spaces - e.g., sparse vector spaces, [named vectors](https://github.com/HarlanH/Named.jl) as in Julia, etc. For simplicity of exposition I've left that out and stuck to `DenseMatrix[Double]` indexed by integers.

Note that a Named Vector implementation would be particularly efficient in the use case given here. The `Map[Name,Int]` could live on the `RealVectorSpace` object rather than the vector itself. Once this implementation choice is made, vector addition/linear transformatoins/etc consists of merely a for-loop and does not require using the `Map[Name,Int]` at all.

# Linear Transformations

Linear transformations are trickier to encode, and unfortunately they carry around a significant bit of boilerplate. It took me quite a few tries before I built a version that would compile:

```scala
case class LinearTransformation[A <: RealVectorSpace, B <: RealVectorSpace](domain: A, range: B) {
  val matrix: DenseMatrix[Double] = DenseMatrix.zeros[Double](domain.dim, range.dim)
  def apply(x: domain.V): range.V = range.V(matrix * x.u)
}
```
This is used as follows:
```scala
val m = LinearTransformation[R3.type, R4.type](R3, R4, DenseMatrix.zeros[Double](3,4))
m(R3.zero) + R4.zero //compiles

m(R4.zero) // type error
m(R3.zero) + R(3).zero //type error, since R(3) is a different vector space than R3
```

Near as I can tell I must provide the unused type parameters `A,B` in order for the compiler to infer the input/output type of `m.apply`. If I remove them, then the compiler is only able to infer that `m.apply` takes an `m.domain.V` as an argument and returns an `m.range.V`. The compiler is unable to deduce that `m.range.V === R4.V`. As always, I'm left waiting for a Sufficiently Smart Compiler (TM).

## The vector space of linear transformations

In principle, it would be nice to encode the vector space of linear transformations as a `RealVectorSpace` - this would enable type safe addition of matrices. I imagine this could be done, I simply haven't put the effort in yet.

# Do you need dependent types?

Another way to solve this problem is with newtype wrappers - this is how Haskell's [Data.Monoid](http://hackage.haskell.org/package/base-4.7.0.1/docs/Data-Monoid.html#t:Sum) package handles things.

```scala
trait VectorWrapper {
  def x: DenseVector[Double]
}
abstract class VectorWrapperVectorSpace[A <: VectorWrapper](aconstructor: DenseVector[Double] => A) extends VectorSpace[Double] {
  def add(u: A, v: A) = aconstructor(u.x+v.x)
  ...
}
class LinearTransformationOfWrappers[D <: VectorWrapper, R <: VectorWrapper](rconstructor: DenseVector[Double] => R, matrix: DenseMatrix[Double])  {
  def apply(u: D): R = rconstructor(matrix * u.x)
}
```

Then whenever you want to enforce type safety on your vectors:

```scala
case class SecurityReturns(x: DenseVector[Double]) extends VectorWrapper
implicit val SecurityReturnsVectorSpace = new VectorWrapperVectorSpace[SecurityReturns](SecurityReturns) {}

val securityReturns = SecurityReturns(DenseVector[Double](...))
///etc
val m = new LinearTransformationOfWrappers[SecurityReturns,Volatilities](Volatilities, DenseMatrix[Double].zeros(...))
```

Extensions to other cases, e.g. `NamedVectors` would be even more verbose.

But verbose or not, this can certainly get the job done. Dependent types are merely functions from values to types - if you are willing to manually inline the body of those functoins, you can certainly do so.

# See also

[The Neophytes Guide to Scala Part 13: Path Dependent Types](http://danielwestheide.com/blog/2013/02/13/the-neophytes-guide-to-scala-part-13-path-dependent-types.html).

[Proving type equality in a Scala pattern match](http://strugglingthroughproblems.blogspot.in/2013/06/proving-type-equality-in-scala-pattern.html)
