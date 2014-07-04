title: Costrong Comonads are Boring
date: 2014-07-09 09:00
author: Chris Stucchio
tags: scala, type systems, scalaz, comonads, category theory
summary: In which I explain a comonad, costrength, and why costrength is both trivial and boring.

After studying monads, a natural topic to turn to next is the [comonad](http://en.wikipedia.org/wiki/Monad_(category_theory)#Comonads_and_their_importance). A `Comonad` is a typeclass with the following methods:

```scala
trait Comonad[F[_]] extends Functor[F] { self =>
  def cobind[A, B](fa: F[A])(f: F[A] => B): F[B]
  def copoint[A](p: F[A]): A
}
```

A `Comonad` must satisfy the laws:

```scala
cobind(fa)(copoint) === fa // left identity
copoint(cobind(fa)(f)) === f(fa) // right identity
```

For comparison, a `Monad` looks similar, but with the location of the `F[_]` reversed:

```scala
trait Monad[F[_]] extends Functor[F] { self =>
  def bind[A,B](fa: F[A])(f: A => F[B]): F[B]
  def point[A](a: A): F[A]
}
```

# Example of a Monad and Comonad - `List` vs `NonEmptyList`

A comonad is best understood via example. Recall that the standard example of a `Monad` is a list. The `bind` operation is `flatMap`:

```scala
def f(x: Int) = List(x, x+1, x+2)
val a = List(1,2,3)

M.point(a) === List(a)
M.bind(a)(f) === List(List(1,2,3),List(2,3,4), List(4,5,6)).flatten
             === List(1,2,3,2,3,4,4,5,6)
```

(The intermediate step above is displayed for clarity purposes.)

The corresponding example of a `Comonad` is the `NonEmptyList` (see [code on github](https://github.com/scalaz/scalaz/blob/series/7.1.x/core/src/main/scala/scalaz/NonEmptyList.scala)) - a list which is guaranteed to have at least one element. The code example above works as follows:

```scala
def f(x: NonEmptyList[Int]) = x.sum
val a = NonEmptyList(1,2,3)

M.copoint(a) === 1 //take out the first element
M.cobind(a)(f) === NonEmptyList(f(NonEmptyList(1,2,3)), f(NonEmptyList(2,3)), f(NonEmptyList(3)))
               === NonEmptyList(6,5,3)
```

So if we think of `F` as a container, we can think of `copoint` as pulling the "first" object out of the container, whereas `cobind` first "un-flattens" the container and then applies `f` to each unflattened-element.

## How the laws make life interesting

After playing around a bit, I came up with the following possible implementation of `cobind`:

```scala
  def pullIn[A](puller: F[_])(pullee: A): F[A] = {
    def constFunc(x: Any) = pullee
    self.map(puller)(constFunc)
  }

  def cobindBoring[A, B](fa: F[A])(f: F[A] => B): F[B] = pullIn(fa)(f(fa))
```

This certainly satisfies the type signature. But it's quite **boring** - I can put `cobindBoring` onto `Functor` if I want to. Given the fancy name, a `Comonad` should be more interesting - turns out it is. This boring version of `cobind` fails the identity law:

```scala
> cobind(NonEmptyList(1,2,3))(copoint)
NonEmptyList(1,1,1)
```

The result should be `NonEmptyList(1,2,3)`. So the Comonad laws force our comonads to be interesting - at the very least, we need more than just any old implementation.

# Costrong Comonads
