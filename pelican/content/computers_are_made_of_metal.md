title: Computers are made of metal (not category theory)
date: 2014-10-01 08:00
author: Chris Stucchio
tags: scala, performance, functional programming
category: programming

Computers are made of metal. It's an important fact to remember. It's wonderful to treat the world as being made of category theory and lambda calculus. The world of math is wonderful and I enjoy it [too much](|filename|costrong_comonads_are_boring.html). But hidden underneath all that lovely abstraction lies a much less beautiful world of semiconductors, cache lines and memory. And you can't forget that.

That's why if you truly want to build a performant system, you need to understand how all that works. And you can't be afraid of putting a little bit of mutable state under the hood - mutable state tends to be vastly faster than copying objects around. It's worth breaking the purity of one's implementation to achieve that.

# The basics

The following is at table reproduced from Peter Norvig's [Teach Yourself Programming in 10 years](http://norvig.com/21-days.html).

<table>
<tr><th>Operation</th><th>Time</th></tr>
<tr><td>execute typical instruction</td><td>1/1,000,000,000 sec = 1 nanosec</td></tr>
<tr><td>fetch from L1 cache memory</td><td>0.5 nanosec</td></tr>
<tr><td>branch misprediction</td><td>5 nanosec</td></tr>
<tr><td>fetch from L2 cache memory</td><td>7 nanosec</td></tr>
<tr><td>Mutex lock/unlock</td><td>25 nanosec</td></tr>
<tr><td>fetch from main memory</td><td>100 nanosec</td></tr>
<tr><td>send 2K bytes over 1Gbps network</td><td>20,000 nanosec</td></tr>
<tr><td>read 1MB sequentially from memory</td><td>250,000 nanosec</td></tr>
<tr><td>fetch from new disk location (seek)</td><td>8,000,000 nanosec</td></tr>
<tr><td>read 1MB sequentially from disk</td><td>20,000,000 nanosec</td></tr>
<tr><td>send packet US to Europe and back</td><td>150 milliseconds = 150,000,000 nanosec</td></tr>
</table>


# Function calls are slow

Functional programming is all about creating and manipulating functions. It's a wonderful abstraction. But it carries a cost. The first thing to recognize:

```scala
val f = (x:Int) => x*x
f: Int => Int = <function1>
```

Anonymous functions are objects, and function calls have overhead. Consider the following code:

```scala
val x: Array[Double] = ... //size 8M
x.map(x => 2.0*x+3.0)
```
The code path is:

1. Create an int pointer `i` into the array, and a result array.
2. Call the anonymous `<function1>` on the value in that array at position `i`.
3. Do the float multiplication/addition.
4. Store the result in a result array.

This takes 240ms.

For comparison, consider this impure (but nearly identical) code:

```scala
val x: Array[Double] = ... //size 8M
var i=0
while (i < x.size) {
  result(i) = 2.0*x(i)+3.0
  i = i + 1
}
```

1. Create an int pointer `i` into the array, and a result array.
2. Do the float multiplication/addition.
3. Store the result in a result array.

This code is **ten times faster** - run time is only 21ms.

Function calls allow you to write shorter code, they are easier to comprehend, and there are many tools to manipulate them. I love functional programming.

But deep inside that functional purity, a tight while loop carefully optimized by the compiler is virtually guaranteed to beat it.

# Object creation is slow

Now lets consider our example code above:
```scala
val x: Array[Double] = ... //size 8M
x.map(x => 2.0*x+3.0)
```

One nice fact about this code is that consecutive elements in the `Array[Double]` are consecutive in RAM. So if the CPU loads a page of `1024` bytes into the CPU cache, then the CPU can perform 128 operations before needing to load a new page into the cache. I.e., the instructions can look like:

1. Load a page of 128 elements into cache.
2. Run the function for those 128 elements.
3. Write the cache line back to RAM.

This involves paging RAM into cache once every 128 elements of the array.

And lets consider a version using a standard functional data structure, the humble list:
```scala
val x: List[Double] = ... //size 8M
x.map(x => 2.0*x+3.0)
```

How long does this take to run?

```
java.lang.OutOfMemoryError: GC overhead limit exceeded
at java.lang.Double.valueOf(Double.java:521)
at scala.runtime.BoxesRunTime.boxToDouble(Unknown Source)
...
```

Fuck if I know. But that code will take 29ms on a 32k array.

This sucks because instead of allocating a single block of ram sized `8 * 1024 * 1024 * sizeof(Double)` long, we are instead allocating `8*1024*1024` nonconsecutive boxes. The relevant class in question:

```scala
final case class ::[B](override val head: B, private[scala] var tl: List[B]) extends List[B] {
  override def tail : List[B] = tl
  override def isEmpty: Boolean = false
}
```

So for each `Double`, we are also creating an object with 2 references (one to the `head`, one to the `tl`). This uses about 3x as much memory. So in terms of low level operations, the worst case here is:

1. Load the page containing `::[Double]` into cache.
2. Look up the head - potentially load that into cache as well.
3. Run an operation on it.
4. Look up the tail - if not already in cache, load it.

There are potentially 3 cache misses **for every element in the list**.

# Trampolining/thunks/laziness is slow

If you are unfamiliar, here is a detailed description of [trampolines](http://blog.richdougherty.com/2009/04/tail-calls-tailrec-and-trampolines.html), and I'm going to steal his example.

Consider a corecursive pair of functions:

```scala
def odd1(n: Int): Boolean = {
  if (n == 0) false
  else even1(n - 1)
}
def even1(n: Int): Boolean = {
  if (n == 0) true
  else odd1(n - 1)
}
```

If you try to call these for large `n`, you will rapidly get a stack overflow.


A trampoline is the following construct:

```scala
sealed trait Bounce[A]
case class Done[A](result: A) extends Bounce[A]
case class Call[A](thunk: () => Bounce[A]) extends Bounce[A]

def trampoline[A](bounce: Bounce[A]): A = bounce match {
  case Call(thunk) => trampoline(thunk())
  case Done(x) => x
}
```

Trampolines are a method used by many strict functional languages to construct lazy streams, as well as simulate tail recursion on the JVM. If I understand things correctly, trampolines are fairly similar to the way Haskell implements laziness via thunks.

Using trampolines, the stack overflow problems can be avoided:

```scala
def even2(n: Int): Bounce[Boolean] = {
  if (n == 0) Done(true)
  else Call(() => odd2(n - 1))
}
def odd2(n: Int): Bounce[Boolean] = {
  if (n == 0) Done(false)
  else Call(() => even2(n - 1))
}
```

But lets think about the cost of doing this. For each value of `n` one must create 2 objects (`Call` and the `thunk`) and call a function. In contrast, consider the following fugly imperative code:


```scala
def even3(n): Boolean = {
  var finished: Boolean = false
  var even: Boolean = true
  var i = n
  while (!finished) {
    if (n == 0) {
      finished = true
    } else {
      even = !even
    }
    i -= 1
  }
  even
}
```

There are precisely 3 objects created - 2 `Boolean`s and an `Int`. No functions are called.

I'm too lazy to run a benchmark on this, but I hope you believe me that it's faster.

# These problems are solveable

In principle, a Sufficiently Smart Compiler (TM) can solve these problems. Such a compiler could properly determine that intermediate steps are unused, merge them (e.g. translate `x.map(f).map(g)` to `x.map(x => g(f(x)))`). Functional purity can make this process a lot safer than in many other languages.

As proof that such things are possible, take a look at [Julia's Benchmarks](http://julialang.org/benchmarks/). Julia is a Lisp-like language designed for numerical code, and it achieves "as fast as C" performance via optional static typing and aggressive compiler optimizations. At some point it is my hope that the more pure functional languages (Haskell, Scala) will adopt similar optimizations and perform similarly.

Until then, we shouldn't forget that computers are made of metal. A few dirty while loops over arrays hidden inside functions, aggressive use of `StringBuilder`, and similar optimizations can drastically speed up performance. Until a Sufficiently Smart Compiler exists, lets not be afraid to dirty up our implementations for the benefit of the users.
