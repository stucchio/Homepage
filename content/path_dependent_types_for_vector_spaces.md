title: Type-safe vector addition with path dependent types
date: 2014-12-02 08:30
author: Chris Stucchio
tags: scala, breeze, dependent types, vector spaces
category: scala
nolinkback: true

The two sides of my programming world have long suffered a disconnect. When I build a robust low latency system, I typically write it in a language like Scala. I make great use of type safety to reduce the number of errors I've made. On the other hand, when I need to do some harcore number crunching, I always go back to Python (and lately sometimes Julia). Unfortunately for me, most of the people hacking on type systems are not focusing their attention on the problems that data geeks run into regularly.

This post illustrates how to use the type system to detect one particular problem I've run into - mixing together vector representations. One possible problem:

```scala
val v3 = DenseVector.zeros[Double](3)
val v4 = DenseVector.zeros[Double](4)
v3 + v4 //RUNTIME ERROR
```

To ensure that this error is caught early, [Breeze](https://github.com/scalanlp/breeze) has a lot of [runtime checks](https://github.com/scalanlp/breeze/blob/master/math/src/main/scala/breeze/linalg/DenseVector.scala#L257).

Here is a more subtle error:
```scala
val securityReturns = DenseVector.zeros[Double](numSecurities)
val pcaRepresentation = DenseVector.zeros[Double](numSecurities)
// do some work
val tmp = pcaRepresentation
val result = securityReturns + tmp
```

See the problem here? No runtime error was raised. But we've done something deeply wrong - we've added together two vectors from different vector spaces that happen to have the same dimension. The number `securityReturns(0)` represents the daily return of the stock symbol AAA. The number `pcaRepresentation(0)` represents the largest contribution to the variance of the returns, and is a weighted sum of the returns of a large number of securities. **The sum of these two is meaningless!**

It's my assertion that we can do better with [path dependent types](http://danielwestheide.com/blog/2013/02/13/the-neophytes-guide-to-scala-part-13-path-dependent-types.html).

# Dependently typed vectors

To begin, we build a wrapper around Breeze's vector space:

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

Then we define the obvious implementation:

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

Even though the dimension is the same, we are not allowed to mix representations.

# Linear Transformations

Linear transformations are trickier to encode.
