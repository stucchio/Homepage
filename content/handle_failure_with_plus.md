title: Handle Failure with MonadPlus/ApplicativePlus
date: 2014-01-19 08:30
author: Chris Stucchio
tags: scala, spire, monads, haskell, scalaz, applicative functor, plus





Handling failure is probably the most important part of building reliable systems. Monads are a common method of encapsulating failure - for instance, `Option[T]` returns either `Some(t)` or `None`, and `None` represents the failure. But Monads do not actually have any mechanism for *handling* failure - in principle, a monad which has failed (whatever failure means) can never be resumed. The same is true for applicative functors.

Nevertheless, recovering from a failure is often desirable. This can sometimes be accomplished via ad-hoc methods on monadic types - e.g., `Option.getOrElse` or `Future.fallbackTo`. But these are less than desirable since they are far from generic - if you want to build a class which is generic in it's functor (e.g. `class FooM[T](monad: Applicative[T])`) you simply cannot recover from a failure.

For this reason, the `Plus` typeclass was created. `Plus` encapsulates types which are a semigroup or monoid in addition to being a functor.



## MonadPlus in Haskell

In Haskell, the primary usage of this pattern is the `MonadPlus` typeclass. It introduces a new operation `mplus :: m a -> m a -> m a` and a new element `mzero :: m a` which must satisfy the following laws:

    mzero `mplus` x == x
    x `mplus` mzero == x
    (x `mplus` y) `mplus` z == z `mplus` (y `mplus` z)

provided of course that both sides can can be evaluated. (It is not always possible to evaluate both sides due to certain infinite structures.)

Additionally, the `MonadPlus` typeclass interacts with the `Monad` typeclass in the following way:

    mzero >>= f == mzero
    x >> mzero == mzero

### Maybe and List

A simple example will illustrate the point of `MonadPlus`.

    Prelude> import Control.Monad
    Prelude Control.Monad> Just 5 `mplus` Just 7
    Just 5
    Prelude Control.Monad> Just 5 `mplus` Nothing
    Just 5
    Prelude Control.Monad> Nothing `mplus` Just 7
    Just 7
    Prelude Control.Monad> Nothing `mplus` Nothing
    Nothing

So with `MonadPlus`, the `mplus` operation basically means "try the first argument, if it fails, fall back to the second argument".

With `List`, `mplus` is simple concatenation:

    Prelude Control.Monad> [2,3] `mplus` [7]
    [2,3,7]

## Plus in Scalaz

Scalaz takes a slightly more complicated approach. A `Plus` trait exists, and it merely represents the fact that a Functor is also a semigroup:

    trait Plus[F[_]]  { self =>
      def plus[A](a: F[A], b: => F[A]): F[A]
    }

Then the `PlusEmpty` represents the fact that this functor is also a monoid:

    trait PlusEmpty[F[_]] extends Plus[F] { self =>
      def empty[A]: F[A]
    }

A Scalaz implicit provides the `<+>` method:

    Some(5) <+> None == Some(5)
    None <+> None == None
    List(2,3) <+> List(7) == List(2,3,7)

And similarly, the `mzero[F[T]]` function provides the zero element:

    mzero[Option[Int]] == None
    mzero[List[String]] == List()

Note that unlike in Haskell, *the monadic structure is not required*. You can have a `Functor` which satisfies `Plus` or `PlusEmpty` even if it is not a Monad.

### Don't confuse <+> and |+|

For every `PlusEmpty` instance, Scalaz provides a `Monoid` instance. But it's important not to confuse the `<+>` and `|+|` operators. Using the standard Scalaz implicits, the latter operator will sometimes build *nested* Monoids:

    Some(1) |+| Some(2) == Some(3)
    Some(1) <+> Some(2) == Some(1)

So in the case of `Option[Int]`, the `<+>` operator represents the fallback operation of the outer functor only. In contrast, `|+|` attempts to make the inner argument into a semigroup as well (if it can). This applies to nested monoids as well:

    Some(Some(1)) <+> Some(Some(2)) == Some(Some(1))
    Some(Some(1)) |+| Some(Some(2)) == Some(Some(3))
    Some(None) <+> Some(Some(2)) == Some(None)
    Some(None) |+| Some(Some(2)) == Some(Some(2))

## Why it's useful

Using the `Plus` typeclass allows you to write functions/classes which are generic in the underlying functor.

A common pattern in scala-land is to build a cache which returns an object wrapped in a functor. For example, [spray caching](http://spray.io/documentation/1.1-M8/spray-caching/) returns values wrapped in a `Future`:

    trait SprayCache {
      def get(k: K)(expr: =>Future[V]): Future[V]
    }

(This is an example that is not identical to the Spray cache.)

On other occasions it might be useful to return a `Validation` or even an `Option`:

    trait OptionalCache {
      def apply(k: K)(expr: =>Option[V]): Option[V]
    }

Now suppose we want to generalize - it's our goal to build a generic `CacheF` trait which parameterizes the functor. I.e., it will be `CacheF[M[_],K,V]` and the `apply` method will return an `M[V]`.
We can, in a very straightforward manner, build such a cache. All you need to implement is the `put` method and the `getFromCache` method, and only the latter of which actually returns an `M[V]`:

    trait CacheF[M,K,V] {
      protected implicit val ap: ApplicativePlus[M]
      def put(k: K, v: M[V]): Unit

      protected def getFromCache(k: K): M[V]

      def get(k: K)(expr: =>M[V]): M[V] = getFromCache(k) <+> {
          val result: M[V] = expr
          put(k,result)
          result
        }
    }

This cache encapsulates the semantics of both the `SprayCache` and the `OptionalCache` - you pull an object out of the cache, and if it's a failure (or if the cache fails to return), then you fall back to actually computing the object. But it's important that all code is shared between both - the only code which isn't is the actual implementation details of `put` and `getFromCache`.

## Math is useful

I've often heard it said that higher math is not particularly useful for programming, at least if you are building CRUD apps. On this point I disagree. Although one can build a CRUD app via basic programming skills and sheer force of will, that doesn't mean knowing a little bit more math is useless. Even when building something as simple as a cache, a little bit of higher math can come in handy and make your code a bit more generic.

P.S. [Injera](https://github.com/stucchio/injera), the library I'm working on uses this pattern in slightly more generality. Go check it out, it might come in handy.
