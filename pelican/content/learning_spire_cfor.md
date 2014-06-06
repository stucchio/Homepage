title: Learning spire - Scala is Slow, cfor helps
date: 2014-01-09 08:30
author: Chris Stucchio
tags: scala, spire, math, array programming
category: scala




Another cool feature offered by [Spire](https://github.com/non/spire) is the `cfor` macro. `cfor` is basically just a C-style for loop:

    cfor(0)(i => i < maxSize, i => i + 1)( i => {
      result = result + i*i
    })

The purpose of `cfor` is not to do anything you can't do with ordinary Scala iterator primitives. The sole purpose of `cfor` is performance, since unfortunately ordinary scala iteration performance is pretty terrible.

I've also written a few other posts on Spire, including this post on [boolean algebras in spire](/blog/2013/learning_spire_boolean_algebra.html) and this post on [vector spaces in spire](http://www.chrisstucchio.com/blog/2013/learning_spire_vector_space.html), which might be useful.



Consider the following problem. We want to apply the affine transformation `(x:Double) => 2.0*x+3.0` to an `Array[Double]`. The idiomatic way to define it is as follows:

    object CFor {
      def mapMultiply(x: Array[Double]): Array[Double] = x.map(x => 2.0*x+3.0)
    }

Now lets benchmark this. We can build a benchmark class using the `scala.testing.Benchmark` library:

    class MultiplyBenchmark(func: Array[Double] => Array[Double]) extends testing.Benchmark {
      var x: Array[Double] = null

      override def setUp() = {
        if (x == null) {
          x = new Array(8*1024*1024)
          cfor(0)(_ < x.size, _ + 1)(i => {
            x(i) = java.lang.Math.random()
          })
        }
      }

      def run = func(x)
    }

    object CForTest {
      val CForTest = new MultiplyBenchmark(CFor.cforMultiply)
      val MapTest = new MultiplyBenchmark(CFor.mapMultiply)
    }

Running this in the console on my machine yields:

    scala> CForTest.MapTest.runBenchmark(100).sum / 100.0
    res2: Double = 240.03

(This number is in milliseconds.)

Suppose we implemented the same function as idiomatic C, translated to Scala:

    def cforMultiply(x: Array[Double]): Array[Double] = {
      val result = new Array[Double](x.size)
      cfor(0)(_ < x.size, _ + 1)(i => {
        result(i) = 2.0*x(i) + 3.0
      })
      result
    }

The identical benchmark runs over 10x faster:

    scala> CForTest.CForTest.runBenchmark(100).sum / 100.0
    res1: Double = 21.42

Now lets consider an example with two arrays:

    def cforMultiply(x: Array[Double], y: Array[Double]): Array[Double] = {
      val result = new Array[Double](x.size)
      cfor(0)(_ < x.size, _ + 1)(i => {
        result(i) = x(i)*y(i)
      })
      result
    }

    def zipMultiply(x: Array[Double], y: Array[Double]): Array[Double] = x.zip(y).map( x => x._1 * x._2 )

The `cforMultiply` takes 26.1ms to run. The `zipMultiply` takes 7.468 *seconds* to run! Holy shit, idiomatic scala is slow.

## Scala - Comparison to Python/Numpy

*Note: A previous version of this post* **incorrectly** *said scala was slower than numpy. I misinterpreted the result of timeit. It is not returning a number in milliseconds, it's returning the time to run all benchmarks as measured in seconds. Thanks to Ichoran and michael_121 for spotting this mistake.*

For comparison, here is multiply in idiomatic python:

    2.0*x+3.0

And the benchmarks:

    In [3]: timeit.timeit('2.0*x+3.0',
                          setup="""from numpy import *;
                                x = random.rand(8*1024*1024)""",
                          number=100)
    <timeit-src>:2: SyntaxWarning: import * only allowed at module level
    Out[3]: 4.537637948989868

This works out to be 45.37ms/run. This is about twice as slow as Scala's `cfor` - I'm guessing because the Scala version iterates once over the array, while the numpy version does so twice.

Dot product implemented as `x*y` takes 27.5ms.

## Using a while loop

[edit: it was suggested I try a while loop after I wrote this] This is equivalent to the performance you would get simply by using a while loop (21.75ms):

    def whileMultiply(x: Array[Double]): Array[Double] = {
      val result = new Array[Double](x.size)
      var i:Int = 0
      while (i < x.size) {
        result(i) = 2.0*x(i) + 3.0
        i += 1
      }
      result
    }

This is because `cfor` is a macro which expands down to the while loop. The implementation can be found [here](https://github.com/non/spire/blob/master/macros/src/main/scala/spire/macros/Syntax.scala#L70), but the gist of it is:

    def oversimplified_cforMacro[A](c: Context)(init: c.Expr[A])
       (test: c.Expr[A => Boolean], next: c.Expr[A => A])
       (body: c.Expr[A => Unit]): c.Expr[Unit] = {

       val tree = q"""
       var $index = $init
       while ($test($index)) {
         $body($index)
         $index = $next($index)
       }
       """
       new InlineUtil[c.type](c).inlineAndReset[Unit](tree)
    }

So using `cfor` is equivalent to using the corresponding `while` loop.

## Lessons learned

**Double check the docs before posting benchmarks. Egg on my face here.** (The previous lesson learned was that numpy was faster than scala+cfor, which is incorrect.)

Another interesting fact I discovered while investigating this is that JVM has built in [bounds check elimination](https://wikis.oracle.com/display/HotSpotInternals/RangeCheckElimination). If the JIT compiler can prove that your loop will not exit the bounds of an array, it will eliminate the range check. If I understand right, it does it whenever your indexing function is linear:

    cfor(0)(i => i < maxSize, i => i + 1)( i => {
      result[a*i+b] = ...
    })

Here the compiler must be able to prove that `a` and `b` are constants.

## Code available

Code for this series of blog posts is available [on github](https://github.com/stucchio/Spire-examples).
