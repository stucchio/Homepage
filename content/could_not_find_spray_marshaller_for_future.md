title: Spray error "could not find implicit value for evidence parameter of type spray.httpx.marshalling.Marshaller[scala.concurrent.Future[_]]"
date: 2014-01-04 21:00
author: Chris Stucchio
tags: scala, spray, marshallers, futures





For various projects I've been using the [spray routing](http://spray.io/) library to provide the web frontend of the recommendation engine. One rather annoying error I've run into several times is the following. Given some type `Foo`, for which a `JsonSerializer` exists, I have cote which looks like the following:

    respondWithMediaType(`application/json`) {
      complete {
        getFooFuture(fooReference)
      }
    }

This results in the error:

    could not find implicit value for evidence parameter
      of type spray.httpx.marshalling.Marshaller[scala.concurrent.Future[Foo]]

I'm writing this blog post in the interest of finding the solution quickly the next time I run into the issue, and maybe it will be helpful for others.



Puzzlingly, the following (slow and inefficient) variation works just fine:

    respondWithMediaType(`application/json`) {
      complete {
        getFoo(fooReference)
      }
    }

The main difference is the type signatures:

    def getFoo(fooRef: FooRef): Foo
    def getFooFuture(fooRef: FooRef): Future[Foo]

In order to trace what the problem is, I put some `implicitly` statements in:

    respondWithMediaType(`application/json`) {
      complete {
        implicitly[Marshaller[Int]]
        implicitly[Marshaller[Foo]]
        implicitly[Marshaller[Future[Int]]]
        implicitly[Marshaller[Future[Foo]]]
        getFooFuture(fooReference)
      }
    }

The first error arises when the compiler reaches `implicitly[Marshaller[Future[Int]]]`. Apparently Spray has forgotten how to serialize `Future[_]` to json, for any value of `_`. In order to serialize a `Future`, spray needs to resolve an implicit `ExecutionContext` which will handle actually running the serialization function.

So if you run into the error, there are basically 3 possibilities.

If the compiler complains about `implicitly[Marshaller[Foo]]`, then the compiler can't find a serializer for the `Foo` type. In this case, you need to define a `jsonSerializer` somewhere, or make sure the existing one is properly imported and marked as implicit.

If the compiler complains about `implicitly[Marshaller[Future[Int]]]`, the problem is that it can't resolve an implicit`ExecutionContext`. This might be because you have no execution context in scope - this is typically resolved by putting `import context.dispatcher` somewhere towards the beginning of the class definition.

The other possibility is that there are *multiple* implicit execution contexts available. This one happened to me because I needed a large mess of boilerplate for various traits I imported, including multiple execution contexts. The solution was to mark one of them as not implicit.
