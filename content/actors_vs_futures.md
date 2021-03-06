title: Don't use Actors for concurrency
date: 2013-12-02 08:00
author: Chris Stucchio
tags: scala, concurrency, actors, futures
category: scala



Don't use actors for concurrency. Instead, use actors for state and use futures for concurrency.

A common practice I've seen in scala code is to use actors for concurrency. This is encouraged by Akka and a lot of writing about Scala, the documentation of which is highly actor-centric. I assert that this is a bad practice and should be considered an antipattern most of the time it is used. Actors should not be used as a tool for flow control or concurrency - they are an effective tool for two purposes, maintaining state and providing a messaging endpoint. In all other circumstances, it is probaby better to use Futures.




Let me emphasize that this is a very scala-specific rant. As I understand it (read: not very well), Erlang is rather different and the distinction between Actors and Futures is not so clear cut.

## The Antipattern

Before continuing, I'll give a concrete example of what I consider to be a bad use of actors:

    class FooActor extends Actor {
      def receive = {
        case (x:FooRequest) => {
          val x = database.runQuery("SELECT * FROM foo WHERE ", x)
          val y = redis.get(x.fookey)
          sender ! computeResponse(x,y)
        }
      }
    }

Elsewhere in the code, `FooActor` is used as follows:

    val fooResult: Future[Any] = fooActor ? FooRequest(...)

The key feature to note about `FooActor` is that *it has no mutable state*. Nothing internal to `FooActor` is altered when it receives a message. However, because `FooActor` is implemented as an actor, Akka has no choice but to run it in a single threaded manner.

Consider now the following alternative code:

    class FooRequester(system: ActorSystem) {
      import system.dispatcher

      def fooResult(x: FooRequest): Future[FooResponse] = Future {
        val x = database.runQuery("SELECT * FROM foo WHERE ", x)
        val y = redis.get(x.fookey)
        computeResponse(x,y)
      }
    }

Elsewhere:

    val fooResult: Future[FooResponse] = myFooRequester.fooResult(FooRequest(...))

### Benefits

The first benefit of using futures rather than actors is that your concurrency situation is drastically improved. Consider the following code:

    val r1 = fooActor ? request1
    val r2 = fooActor ? request2
    for {
      result1 <- r1
      result2 <- r2
    } yield (combination(result1.asInstanceOf[FooResponse], result2.asInstanceOf[FooResponse]))

This code appears to be running in parallel. The futures `r1` and `r2` are, in principle, computed separately. But due to the single-threaded nature of the `fooActor`, the computation is still single threaded. In contrast, with Futures the computation is now multithreaded:

    val r1 = myFooRequester.fooResult(request1)
    val r2 = myFooRequester.fooResult(request2)
    for {
      result1 <- r1
      result2 <- r2
    } yield (combination(result1, result2))

 A second benefit is easy type safety, though of course that can also be accomplished via [typed actors](http://doc.akka.io/docs/akka/2.2.3/scala/typed-actors.html).

**Side note:** For those unfamiliar with Akka futures, one might ask why I used this convention. Why didn't I simply write it like this?

    for {
      result1 <- myFooRequester.fooResult(request1)
      result2 <- myFooRequester.fooResult(request2)
    } yield (combination(result1, result2))

The answer is that the former will run concurrently, while the latter will only run serially. The latter case is equivalent to:

    myFooRequester.fooResult(request1).flatMap( result1 =>
      myFooRequester.fooResult(request2).flatMap( result2 =>
        combination(result1, result2)
      )
    )

Written this way it is clear that `myFooRequester.fooResult(request2)` is only evaluated when `result1` becomes available.

### Other routes to concurrency

Another way to gain concurrency using actors would be to spin up multiple actors and put them behind a [router](http://doc.akka.io/docs/akka/2.2.3/scala/routing.html). This will give a certain degree of concurrency, but is unnecessarily complicated.

It also violates separation of concerns. Fundamentally, handling concurrency is the role of the [ActorSystem](http://doc.akka.io/docs/akka/2.2.3/general/actor-systems.html). If a particular method of handling this is needed (e.g., turning a `FooRequest` into a `FooResponse` requires blocking calls and a limited number should be run simultaneously), this should be handled by the `ActorSystem`.

Lets be concrete. Suppose that for whatever reason, no more than 10 database queries should be running simultaneously. If we use Actors to manage concurrency, there are two places this must be configured - in the `ActorSystem` itself, and in the `Router` which routes requests to the actors. Suppose the database were upgraded and could now handle 20 concurrent queries. If we only increase the thread limit in the actor system but forget to increase the number of actors, we will continue running only 10 concurrent queries.

But really, you shouldn't use your `ActorSystem`'s thread pool to manage the number of concurrent database queries either. Your `ActorSystem` should manage your `Thread` resources - your database connection pool should actually be what is used to manage database concurrency. It's highly unlikely that your home grown concurrency system will be faster than [BoneCP](http://jolbox.com/).

In contrast, if we used futures, then the change need only be made in one place.

## Actors are for state

Consider now the problem of counting. It is very straightforward to use an Actor for this:

    class FooCounter extends Actor {
      var count: Long = 0

      def receive = {
        case Foo => { count += 1}
        case FooCountRequest => { sender ! count }
      }
    }

This is the proper use of Actors. The sole responsibility of the `FooCounter` is to maintain the internal state, specifically the `var count`.

In contrast, handling this with Futures would be difficult - concurrency primitives (in this case, a `java.util.concurrent.AtomicLong`) object would need to be used to maintain the state and there would likely be contention if different futures modified the same object.

(Tangentially, for those unfamiliar with Akka, although it appears public the variable `count` is in fact private. The actual `FooCounter` object is never exposed to the outside world - only an `ActorRef` object is. If you call `actorRef ! message`, this will result in the `receive` method being applied to message, but this is handled by Akka rather than directly.)

## Caching is not state

An important fact about maintaining state is that it changes:

    fooCounter ! Foo
    fooCounter ! FooCountRequest
    //scalatest code indicating that fooCounter should respond with the message 1
    expectMsg() { case 1 => true }

    fooCounter ! Foo
    fooCounter ! FooCountRequest
    expectMsg() { case 2 => true }

Caching does not meet this criteria, except as an implementation detail. Consider a `BarCacher` actor:

    barCacher ! BarRequest(1)
    expectMsg() { case BarResponse(1) => true }

    barCacher ! BarRequest(1)
    expectMsg() { case BarResponse(1) => true }

Under no circumstances should `barCacher` ever return a different result, unless of course the cache becomes invalidated.

Furthermore, if an actor is used for caching, a single thread for both reads and writes becomes absolutely necessary.

In contrast, consider the [Spray caching](http://spray.io/documentation/1.2-M8/spray-caching/) approach to caching in the Akka world. Whenever a cached operation is invoked it returns a `Future[T]` object. This `Future[T]` object is immediately placed in the cache before it has actually become ready. So consider the following sequence:

    # time = 0
    val future = cachedOp()
    val present = Await.result(future, 10 seconds)
    # terminates at time=1000ms

Now consider a separate thread:

    # time = 500ms
    val future2 = cachedOp()
    val present2 = Await.result(future, 10 seconds)
    # terminates at time=1000ms, not 1500ms

The first thread waits 1000ms for the future to finish while the second thread only waits 500ms. At the level of memory (and cpu cache locality), both threads of execution view the exact same `Future[T]` object. Additionally, the underlying data structure (a [ConcurrentLinkedHashMap](https://code.google.com/p/concurrentlinkedhashmap/)) suffers contention only on write, not on read (except when evicting entries), which is far more scalable than the single-threaded performance of an actor.

## Futures are composable

A very nice feature of Futures is that they are highly composable. Consider the following problem. I want to return an HTTP result to a user based on the following criteria:

- If a cookie is set, I'll return them a result from the cookie.
- If I have seen the user before but they have no cookie, I probably stored a result in Redis. I'd like to return that result.
- If neither of the previous two criteria holds, I'd like to build them a result from scratch. This is time consuming and requires a database hit, provided a result is not in the cache.

With futures, the code to do this is:

    def processRequest(request: HttpRequest): Future[HttpResponse] = {
      val fromRequest: Option[HttpResponse] = getFromCookie(request)
      fromRequest.map( r => Future { r }).getOrElse({
        val fromRedis = getFromRedis(request)
        //getFromRedis will return an unsuccessful future object if redis does not contain anything
        val fromScratch = getFromScratch(request)

        //On any error in fromRedis, build from scratch
        val result = fromRedis.recoverWith({ case _ => fromScratch })

        result
    })

In short, we have put together this complex logic with just a little bit of functional composition. Now suppose we want to deal with additional issues. For example, error logging is handled by putting this line of code anywhere before the last line:

      //Error Handling - log message runs in separate thread
      result.onFailure({ case e => log.error("OMFG, NOOOO! This error {} occurred", e) })

Suppose also that we want to warm the cache based on the `fromScratch` value. We simply add this line of code somewhere:

      //Warm the cache without making the request wait
      fromScratch.foreach( value => cache.put(request, value)

This is handled in a separate thread, i.e. the user may have their HTTP request returned *before* the result has actually been put into Redis. Only the critical path of computation needs to run before returning the result to the user - the rest can happen out of band.

Handling this with actors would be a bit trickier. One would need to translate essentially functional code into Java-style [Kingdom of Nouns](http://steve-yegge.blogspot.co.uk/2006/03/execution-in-kingdom-of-nouns.html) code - build a `class CacheWarmer`, a `class FailureLogger`, etc.

## Actors as a message endpoint

Another important use for actors is to be a message endpoint. The best example of this is [Spray Routing](http://spray.io/documentation/1.2-M8/spray-routing/) actors. They are used as follows:

    val myHttpServer = system.actorOf(Props(new MyHttpServer), "http-server")
    IO(Http) ! Http.Bind(myHttpServer, "localhost", port=8080)

The internals of `myHttpServer` will usually be extremely functional:

    class MyHttpServer extends Actor with HttpService {
      val routes = {
        get {
          path("foo" / Segment) { fooSlug =>
            respondWithStatus(StatusCodes.OK)( ctx => {
              ctx.complete( computeHttpResponse(fooSlug) )
            })
          }
        }
      }
    }

In this example, `MyHttpServer` is not encapsulating state (although in principle it could). It's sole purpose here is to act as a messaging endpoint. Actors internal to `IO(Http)` can send messages to an `ActorRef` representing `myHttpServer`, and further delegation is the responsibility of that actor. This is nearly always best accomplished by having `MyHttpServer` make purely functional calls to external methods that return `Future[HttpResponse]` objects.

## Conclusion

Actors are awesome. But they aren't the only abstraction we have. Futures are another great abstraction which work very well with purely functional code. Actors are great for maintaining state, futures are great for everything else.

P.S. In the [reddit thread](http://www.reddit.com/r/scala/comments/1sa888/use_actors_for_state_and_futures_for_concurrency/) on this post, eigenfutz (now [deleted]) raised the concern that the quantity of work being performed by threads is uncontrollable. I don't believe his points arguing for actors over futures are valid (and explain why there), but the discussion is useful nonetheless. In particular, it is a good argument for [work pulling](http://blog.goconspire.com/post/64901258135/akka-at-conspire-part-5-the-importance-of-pulling).
