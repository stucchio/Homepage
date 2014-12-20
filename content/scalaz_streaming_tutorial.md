title: Scalaz Stream - a Functional Reactive Programming Tutorial
date: 2014-09-15 08:30
author: Chris Stucchio
tags: scala, scalaz, scalaz-streaming, concurrency, reactive, coreactive
category: scala
nolinkback: true

[Scalaz Stream](https://github.com/scalaz/scalaz-stream) is a relatively new concurrency and dataflow library for Scala. Near as I can tell, it's single-box use cases are the same as Akka's, provided you don't plan to build a distributed system. I've been struggling to learn the library, and figured I'd write down my thoughts in the hopes of making other people's learning experience easier.

# Process

The core object in Scalaz Stream is the `Process[F[_], X]`. A process can be thought of as a stream of values of type `X` together with an effect system of type `F[_]`. The typical case will take `F[_]` to be `Task[_]`, but that is not fundamentally necessary. For those unfamiliar with `Task`, here is a great [tutorial](http://timperrett.com/2014/07/20/scalaz-task-the-missing-documentation/) on it.

The idea of a `Process` is that you can run the `Process` via one of several `run` methods, and this will process the stream in the `F[_]` effect system. Lets look at some (oversimplified - look [here](https://github.com/scalaz/scalaz-stream/blob/master/src/main/scala/scalaz/stream/Process.scala) for the real ones) type signatures:

```scala
trait Process[F[_], X] {
  ...
  def run(implicit m: Monad[F]): F[Unit]
  def runLast(implicit m: Monad[F]): F[X]
  def runLog(implicit m: Monad[F]): F[IndexedSeq[X]]
}
```

The `run` method runs the process but discards the result - the only reason to run the computation is for it's effects (which are captured by `F`). The `runLast` method runs the stream and captures it's *last* value, as well as it's effects. The `runLog` method runs the process, captures it's effects *and* captures a log of the entire stream. (Yes, `runLog` can use a LOT of memory.)

To start with, lets look at a `Process[List,Int]`. The *effect* of the `List[_]` monad is that a list of values is returned. In this example, `Process.range(0,10)` returns a `Process` which generates the numbers between 0 and 10.

```
scala> val p: Process[List,Int] = Process.range(0,10)

scala> p.run
res5: List[Unit] = List(())

scala> p.runLast
res10: List[Option[Int]] = List(Some(9))

scala> p.runLog
res11: List[IndexedSeq[Int]] = List(Vector(0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
```

If one wanted to do more complex effects, one would replace `List[_]` with `IO[_]` or `DatabaseTransaction[_]`, or whatever.

# Starting a Process

In Scalaz Streaming, there are a variety of ways of creating a `Process`. The simplest, albeit most boring:

```scala
scala> import scalaz.stream.io
scala> val p = Process(1,2,3,4,5)
p: scalaz.stream.Process[Nothing,Int] = Emit(WrappedArray(1, 2, 3, 4, 5))
```

Scalaz streaming provides a few analogues of standard scala methods:

```scala
val lns: Process[Task,String] = io.linesR("inputfile.txt")
```

This is exactly what it looks like - a stream comprised of the lines of an input file. The monad here is `Task`, which is Scalaz's version of `Future` - again, go [read the tutorial](http://timperrett.com/2014/07/20/scalaz-task-the-missing-documentation/).

Another way to create a process is via `scalaz.stream.async.Queue`. This is done as follows:

```scala
import scalaz.stream._

val q = async.unboundedQueue[String]

while (true) {
  val inputString = readFromTheNetwork()
  q.enqueueOne( inputString ).run
}

//...elsewhere...

val stringsFromTheNetwork: Process[Task,String] = q.dequeue
```

This is how you write procedural code to interface with java/scala libraries (e.g. servlets, akka), and put it into Scalaz Stream. The `stringsFromTheNetwork` variable is the resulting stream. Other methods include:

```scala
val f: Task[A] = Task.async { ... } //Do something to create an object
val repeatedF: Process[Task,A] = Process.repeatEval(f) //Do it again and again
```

Another tool for creating `Process[Task,A]` objects is signals:

```scala
import scalaz.stream.async

val signal = async.signal[Boolean]
val signalChanges: Process[Task,Boolean] = signal.discrete

//Thread 1
signal.set(true).run // Time = 1
signal.set(true).run // Time = 2
signal.set(false).run //Time = 3
...
//Thread 2
signalChanges.map(x => {
  println("" + x + " -> " + System.currentTimeMillis)
  }).run.run
// Will print:
// true -> 1
// false -> 3
```

Another useful method in realtime operations is `Process.awakeEvery`:
```scala
import scala.concurrent.duration._
val clock = Process.awakeEvery(1 seconds)
```

Every second, a new value will enter the `clock` process, namely `1 seconds`, `2 seconds`, `3 seconds`, etc (the actual values may vary a little bit).

### What's with `process.run.run`?

The astute reader might be wondering why I did `process.run.run`. Was it a typo? Did I intend to do `process.run` (no)? The reason is this - we are invoking `run` first on the `Process[Task,_]` object, and second on the `Task[_]` object itself.

```
scala> process
res0: Process[Task,Boolean]

scala> process.run
res1: Task[Unit]

scala> process.run.run
res2: Unit
```

So the first invocation of `run` is `Process.run`, and results in a `Task[Unit]`. The second `run` is `Task.run`. Another way to see it:

```
scala> process
res0: Process[Task,Boolean]

scala> process.runLast
res1: Task[Option[Int]]

scala> process.runLast.run
res2: Option[Int]
```

# Manipulating the process

So great. We've got a stream of values. What do we do with it?

As you might expect, all the standard Scala functional programming methods are supported:

```scala
val p: Process[Task,Int] = Process.range(0,10)

val mapResult = p.map(x => "the value is " + x).runLog.run
// Vector("the value is 0", "the value is 1", ...)

val filterResult = p.filter(x => x % 2 == 0).runLog.run
Vector(0, 2, 4, 6, 8)
```

The `flatmap` method is a bit trickier, since it operates at the `Process` level:

```scala
p.flatMap(x => Process(x, x-1)).runLog
// Result: Vector(0, -1, 1, 0, 2, 1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 6, 8, 7, 9, 8)
```

These are all interesting, but none actually allow us to run a real streaming computation. To do many interesting operations we need to be able to build a general [causal function](http://en.wikipedia.org/wiki/Causal_system). A causal function is a function that depends on the past and present (i.e., earlier values in the stream) but not the future. This can be accomplished with the `scan` method:

```scala
val runningTotal = p.scan(0)( (state, newValue) => state + newValue)
// Vector(0, 0, 1, 3, 6, 10, 15, 21, 28, 36, 45)
// Vector(initialState, initialState + firstElement, initial state + firstElement + secondElement, etc)
```

So in principle, `process.scan(initialState)( (state, input) => state)` is the Streaming equivalent of building a stateful actor (e.g. Akka style) and having that actor process a stream of values.

Processes can be zipped together:

```scala
val lettersAndNumbers = (Process.emitAll(List(1,2,3)) zip (Process.emitAll(List("a", "b", "c"))
// Process contains (1,a), (2,b), (3,c)
```

# Combining streams

Streams can be combined in a variety of ways. One tool is the Wye (named after the Wye rail). A wye is a tool for merging streams. For example, one method it has is `dynamic`. This method takes two functions, one function of the left stream, the other of the irght stream, and it uses these functions to determine which stream to receive from next. A simple example which alternates between streams:

```scala
val l = Process.emitAll(List(1,2,3,4,5))
val r = Process.emitAll(List("a", "b", "c", "d", "e"))

val w = wye.dynamic((x:Int) => wye.Request.R, (y:String) => wye.Request.L)

l.wye(r)(w).runLog.run
// Result is Vector(ReceiveL(1), ReceiveR(a), ReceiveL(2), ReceiveR(b), ReceiveL(3), ReceiveR(c), ReceiveL(4), ReceiveR(d), ReceiveL(5), ReceiveR(e))
```

Another version - this one only requests from the right stream whenever the left element is divisible by three:

```scala
val w = wye.dynamic((x:Int) => if (x % 3 == 0) { wye.Request.R } else { wye.Request.L }, (y:String) => wye.Request.L)

l.wye(r)(w).runLog.run
/// Result is Vector(ReceiveL(1), ReceiveL(2), ReceiveL(3), ReceiveR(a), ReceiveL(4), ReceiveL(5))
```

# Putting the pieces together: an example

Lets now consider the following situation. We receive an incoming stream of true/false events. We want to keep a rolling total of both the number of events, and the number which were true. Separately, we have a stream of incoming requests, and for each request we want to return the current value of `(allEvents, trueEvents)`.

So consider the first stream as input data, and the second stream as a monitoring process.

To begin we have our source:

```scala
val input: Process[Task,Boolean] = Process.awakeEvery(300 milliseconds)(Strategy.DefaultStrategy, Strategy.DefaultTimeoutScheduler).map(_ => (math.random < 0.3))
```

We will use the `scan` method to keep track of the current counts:
```scala
val counter = input.scan( (0L,0L) )( (count, event) => ( count._1+1, count._2 + (if (event) { 1L } else { 0L }) ) )
```

We will then want to generate a `Signal` which is always set to the current value of the counts:

```scala
import scalaz.stream.async

val sig = async.signal[(Long,Long)]
val snk = sig.sink
val counterToSignal = counter
        .map( x => async.mutable.Signal.Set( x ) : async.mutable.Signal.Msg[(Long,Long)] )
        .to(snk)

Task.fork( generator.run ).runAsync( _ => () ) //Run this in a separate thread
```

The `async.mutable.Signal.Set(x)` is a message which, when received by a `signal.sink`, will set the signal to `x`. Ok, we are now tracking statistics.

The other side of the process, which takes requests and returns responses, is a bit trickier. First consider the stream of requests:

```scala
val requestSignal = Process.awakeEvery(1000 milliseconds)(Strategy.DefaultStrategy, Strategy.DefaultTimeoutScheduler)
```

To combine the request stream and the statistics signal, we use a `Wye`:

```scala
val w = wye.dynamic( (_:Any) => wye.Request.R, (_:Any) => wye.Request.L)

val responseStream = requestSignal.wye(stateSignal)(w).filter( _.isR ).map(_ match {
      case ReceiveY.ReceiveR(x) => x
      case _ => ???
    }).map(x => println("Response " + x))
```

The `responseStream` will now a output a response whenever a request is received. Typical output:

```
scala> responseStream.run.run
Response (3,2)
Response (6,3)
Response (9,4)
Response (13,5)
Response (16,6)
Response (19,7)
Response (23,8)
Response (26,8)
Response (29,11)
Response (33,13)
```

# Performance

This is where the story becomes less than pretty. Here is a fairly straightforward benchmark, comparing Scalaz Stream to it's closest competitor - Akka. I build a wrapper class `case class Wrapper(x: Long, y: Long)` with a `+` method that behaves in the obvious way and compute a rolling sum of `1024*1024` wrappers. In stream, it's done as follows (full code):

```scala
q.dequeue.scan(Wrapper(0,0))( (state, w) => (state + w) ).scan(0L)( (count, w) => {
  if (count == finishCount) {
    finishTime = System.currentTimeMillis
  }
    count + 1
})
```

In Akka the code is [considerably longer](https://gist.github.com/stucchio/fbc29e84f68817b0a798), but more or less similar - just using Actors to handle the state. In Akka the whole process takes about 10 seconds. In Scalaz Stream, the process takes 42 seconds. I'm not sure if this is due to Scalaz Stream or perhaps just my current inability to write performant code in it. However, stream can definitely be sped up - a little playing around gave me [this pull request](https://github.com/scalaz/scalaz-stream/pull/237#issuecomment-55305291) which makes `Process.map` about 10x faster than before.

Browsing the source code, it appears that Scalaz Stream certainly does a lot of object creation (some of it appears unnecessary), probably more than Akka. On the other hand it hits thread pools less. In principle (perhaps by polluting the innards of Scalaz Stream with some imperative code) it should be possible to improve performance.

# See also

You must read [Task: The Missing Documentation](http://timperrett.com/2014/07/20/scalaz-task-the-missing-documentation/).

Paul Chiusano (author of Scalaz-Stream) has a useful [slideshow on it](http://pchiusano.github.io/talks/scalaz-stream-nescala-2014/scalaz-stream-nescala-2014.html#/an-introduction-to-scalaz-stream), albeit one or two versions out of date.

[Scalaz Stream - Reactive in Reverse](https://dl.dropboxusercontent.com/u/1679797/NYT/Reactive%20in%20Reverse.pdf) is also worth reading. This slideshow emphasizes how Scalaz Stream is pull rather than push.

I also wrote about [Agents - a purely functional alternative to actors](|filename|agents.md), which is a thin library on top of Scalaz Stream.
