title: Scalaz Streaming tutorial
date: 2014-09-10 09:00
author: Chris Stucchio
tags: scala, scalaz, scalaz-streaming, concurrency
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

## Starting a Process

In Scalaz Streaming, there are a variety of ways of creating a `Process`. Scalaz streaming provides a few analogues of standard scala methods:

```scala
import scalaz.stream.io

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

This is how you write procedural code to interface with java/scala libraries (e.g. servlets, akka), and put it into Scalaz Stream. The `stringsFromTheNetwork` variable is the resulting stream.
