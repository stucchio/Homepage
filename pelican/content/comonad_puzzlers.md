title: Comonad puzzlers
date: 2014-07-09 09:00
author: Chris Stucchio
tags: scala, type systems, scalaz, comonads
summary: Random musings about Comonads which may help the reader to better understand them.

Like many before me, I recently began pondering the age old question: what is a `CoApplicative`? And like everyone else, I got nowhere. But along the way, I ran into some interesting questions about `CoMonad` which helped shed some light on the nature of this structure. I warn the reader - this post may be a bit stream of consciousness.

A `Comonad` is a typeclass with the following methods:

```scala
trait Comonad[F[_]] extends Functor[F] { self =>
  def cobind[A, B](fa: F[A])(f: F[A] => B)
  def copoint[A](p: F[A]): A
```

If we think of `F` as a container, we can think of `copoint` as pulling an object out of the container. The details of `cobind` are a little more complicated, and the rest of this post will attempt to provide some explanation.

A `Comonad` must satisfy two laws:

```scala
cobind(fa)(copoint) === fa // left identity
copoint(cobind(fa)(f)) === f(fa) // right identity
```

# A boring `cobind`

After playing around a bit, I came up with the following possible implementation of `cobind`:

```scala
  def pullIn[A](puller: F[_])(pullee: A): F[A] = {
    def constFunc(x: Any) = pullee
    self.map(puller)(constFunc)
  }

  def cobind[A, B](fa: F[A])(f: F[A] => B): F[B] = pullIn(fa)(f(fa))
```

This certainly satisfies the type signature. But it's quite boring - I can make this `cobind` definition a method on `Functor`. Surely a `Comonad` must be more interesting.

It turns out it is more interesting - the boring version of `cobind` fails the identity law:

```scala
> cobind(NonEmptyList(1,2,3))(copoint)
NonEmptyList(1,1,1)
```

The result should be `NonEmptyList(1,2,3)`.

It's not always true that once you get things to compile, your code is probably correct.

# Decisive functors
