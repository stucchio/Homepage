title: Costrong Comonads are Boring
date: 2014-07-04 09:00
author: Chris Stucchio
tags: scala, type systems, scalaz, comonads, category theory
summary: Strength is a category theoretical property which is known to be *boring* - every `Monad` in `Hask` (and similarly `Scal`) satisfies it. The question arises - what about it's dual, Costrength? What would a Costrong Comonad look like? Is it interesting? It turns out the answer is no - every `Comonad` in `Hask`/`Scal` is `Costrong`. In this post I'll provide a brief tutorial on `Comonads` and show why every `Comonad` is also Costrong. You do NOT need to know much category theory to follow this post, but some familiarity with the everyday programming of Monads will be helpful.

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

# Strong Monads and Costrong Comonads

A [strong monad](http://en.wikipedia.org/wiki/Strong_monad) is a monad with an additional function:

```scala
trait Strong {
  def strengthen[A,B](fa: (A,F[B])): F[(A,B)]
}
```

There are 4 laws a Strong Monad must satisfy - the [wikipedia page](http://en.wikipedia.org/wiki/Strong_monad) displays them as commutative diagrams. A Costrong Comonad has a complementary definition:

```scala
trait Costrong {
  def costrengthen[A,B](fa: F[Either[A,B]]): Either[A,F[B]]
}
```

What this definition means is that we can co-strengthen the type of `fa` - it's either an `A` or else it's an `F[B]`.

One computational way to interpret this is that the result is `Either` a result of type `A`, or else it's an error wrapped in `F[B]`.

The laws a `Comonad` must satisfy can be derived by looking at the commutative diagrams on wikipedia and reversing the arrows. When doing this process, the product type `(A,B)` is replaced by the sum type `Either[A,B]`. The basic laws of a `CostrongComonad` are (in addition to the usual `Comonad` laws):

```scala
costrengthen(self.map(fb)(x => Right(x): Either[A,B])) === Right(fb)
costrengthen(fab).bimap(x=>x, copoint _) === copoint(fab)
```

There are also a couple of more complicated laws about associativity:

```scala
costrengthen(fab).bimap(x => x, cojoin _) === costrengthen(self.map(self.cojoin(fab))(costrengthen _))
eassoc(costrengthen(fabc).bimap(a => a, costrengthen _)) === costrengthen( self.map(fabc)(eassoc) )

where

def eassoc[A,B,C](eabc: Either[A,Either[B,C]]): Either[Either[A,B], C] = eabc match {
  case Left(a) => Left(Left(a))
  case Right(Left(b)) => Left(Right(b))
  case Right(Right(c)) => Right(c)
}
```

In one of the few posts I've seen discussing the topic, [Edward Kmett](http://comonad.com/reader/2008/deriving-strength-from-laziness/) shows that in the category `Hask`, all monads are strong and thus strength is boring. When trying to implement `Costrong`, I discovered that costrong comonads are also boring.

The reason why is very simple - every `Comonad` which is also a `Functor` also satisfies `Costrong`:

```scala
implicit def CostrongOfComonad[F[_]](m: Comonad[F]): Costrong[F] = new Costrong {
  def costrengthen[A,B](fa: F[Either[A,B]]): Either[A,F[B]] = fa match {
    case Left(a) => Left(a)
    case Right(b) => Right( m.map(fa)( eab => eab.bimap(_ => b, x => x)) )
  }
}
```

In `Hask` and `Scal`, of course, every `Comonad` is also a `Functor`.

In terms of `NonEmptyList`, what does this look like?

```scala
costrengthen(NonEmptyList(Left("oops"), Right(1), Right(2))) === Left("oops")
costrengthen(NonEmptyList(Right(0), Left("oops"), Right(2))) === Right(NonEmptyList(0, 0, 2))
```

It essentially takes a container, looks at the `copoint` of the container, and replaces all `Left(...)` instances by the copoint while simply unwrapping the `Right` elements.

The only properties I used when creating the `Costrong` object were `Comonad.copoint` and `Functor.map` - no additional work is necessary.

## `costrengthen` is not unique

Consider another way of achieving a similar result. Rather than replacing the `Left(...)` instances with `b`, we might simply remove them:

However, the `costrengthen` function is not unique. Another possible definition for `NonEmptyList`:

```scala
def costrengthen[A,B](fab: NonEmptyList[Either[A,B]]): Either[A, NonEmptyList[B]] = copoint(fab) match {
  case Left(a) => Left(a)
  case Right(b) => Right({
    val filtered = fab.list.flatMap( _ match {
      case Left(_) => List[B]()
      case Right(bb) => List(bb)
    })
    new NonEmptyList(b, filtered.tail)
  })
}
```

Running tests shows that this definition also satisfies the `CostrongComonad` laws.

# Is there some interesting definition of `SemiCostrongComonad`?

In his post on [strength](http://comonad.com/reader/2008/deriving-strength-from-laziness/), Edward Kmett poses a different definition of `costrengthen`. He proposes that if there are *any* left elements in the container, return one of them. Otherwise, return the container after unwrapping the right elements.

I like this definition. But unfortunately it fails the second `CostrongComonad` law:

```scala
costrengthen(fab).bimap(x=>x, copoint _) === copoint(fab)
```

The counterexample is easy to see:

```
val x = NonEmptyList(Right(1), Left("oops"))
costrengthen(x).bimap(x => x, copoint _) === Left("oops").bimap(x => x, copoint _)
                                         === Left("oops")

copoint(x) === Right(1)
```

But here is a puzzle I'm posing: is there an alternate category theoretical construct, which I'll label `SemiCostrongComonad`, which is more interesting? Some definition which Edward Kmett's proposed `costrengthen` will actually satisfy?

# Conclusion

In programming languages like Scala and Haskell, `Costrong` is a boring property for a `Comonad` to posess. Any `Functor`, which includes every `Comonad` satisfies this property. So if we are looking for interesting behaviors to add to a library like scalaz or the Haskell prelude, Costrength is not it.

Anyone who wants to play with these concepts can find my [code on github](https://github.com/stucchio/scalaz/tree/costrong).
