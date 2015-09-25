title: I don't understand JVM performance
date: 2014-03-10 09:00
author: Chris Stucchio
tags: scala, breeze, spire, jvm, performance, arrays





I've been hacking on [Breeze](https://github.com/scalanlp/breeze) lately, which is a scientific library for Scala which aims to replace [Scipy](http://scipy.org). It's got a long way to go, but it's definitely a great library and one that I make significant use of. One of the great things about using the same language that your scientific library is written in is that you don't need to take a huge (10-100x) performance hit when you need to drop down to using a for loop.

Nevertheless, it's still good if your low level for-loop performance is good. I've spent a few days optimizing the low level array access code in Breeze, and I've run into a puzzle.




# The original implementation

An important fact about Breeze's `DenseVector` is that there is not a 1-1 correspondence between a `DenseVector` and an `Array`. A `DenseVector` refers to a subset of an array, specified by an `offset` and a `stride`. For example, you can have a `DenseVector` of size `1024` with an underlying array of size `3*1024` - the vector might have `offset=1024` and `stride=2`, in which case the data is stored at `array(1024), array(1026), array(1028), etc`.

The implementation of Breeze's `DenseVector.update` was the following:

    def update(i: Int, v: E) = {
      if(i < - size || i >= size) throw new IndexOutOfBoundsException(i + " not in [-"+size+","+size+")")
      val trueI = if(i<0) i+size else i
      data(offset + trueI * stride) = v
    }

In addition to supporting `offset` and `stride`, this does two interesting things. First, it allows negative array access - `denseVector.update(-1, 12)` sets the *last* element of the array to 12. Second, it creates a nicer error message if you go out of bounds.

It's also fairly slow. The following benchmark code takes 9.3 microseconds on an 8k `Array[Double]`:

    var i=0;
    while (i < vec.size) {
      vec.update(i, i.toDouble)
      i += 1
    }

# Negative indices?

The standard `update` method also does a lot of unnecessary work when the programmer has already checked the array bounds, as is done in the above benchmark (and as is done in a lot of real code). There are two bounds checks - the explicit one in the `update` code, and the implicit one that comes with the normal Java `Array`. Additionally, there is a branch depending on whether `i < 0`, and possibly an extra addition to compute `trueI`.


## The JVM and Bounds Check Elimination

One nice feature about the JVM is that although array access is bounds checked, the JVM is smart enough to eliminate it some of the time. Oracle has a nice page on [Range Check Elimination](https://wikis.oracle.com/display/HotSpotInternals/RangeCheckElimination). The conditions under which it works are the following:

**First:** The array being accessed must not be reallocated in the body of the loop. You can't do this:

    vec = new Array[Double](1024)

**Second:** The index variable must have constand stride. I.e., this is ok:

    while (i < vec.size) {
      i += 3
      ...
    }

This is not ok:

    while (i < vec.size) {
      i += if (i % 2 == 0) { 3 } else { 5 }
      ...
    }

**Third:** The array index must be a *linear* function of of the index. This is valid:

    vec(offset+i*stride)

This is not:

    val trueI = if(i<0) i+size else i
    data(offset + trueI * stride) = v

Because of the if-statement, the array access is only piecewise linear.

## A better dense vector update method

In order to exploit range check elimination, I created a much simpler `unsafeUpdate` method:

    def unsafeUpdate(i: Int, v: E): Unit = { data(offset + i * stride) = v }

With this method, which no longer allows negative indexes, the benchmark takes about 7.5 microseconds. Better, but far from optimal.

One thing I noticed which is often unnecessary is the fact that the accessor is `offset+i*stride`. In many use cases, `offset == 0` and `stride == 1`. So I tried to eliminate that calculation for the case of simple vectors:

    private val isSimpleVector = (offset == 0) && (stride == 1)
    def unsafeUpdate(i: Int, v: E): Unit = if (isSimpleVector) { data(i) = v} else { data(offset + i * stride) = v }

Didn't work - performance became worse, probably because the if-statement is breaking range check elimination.

I tried another approach:

    private val innerUpdate: ((Int,E) => Unit) = if ((offset == 0) && (stride == 1)) { (i:Int,v:E) => {data(i) = v} } else {(i:Int,v:E) => {data(offset+i*stride)=v}  }
    def unsafeUpdate(i: Int, v: E) = innerUpdate(i,v)

Before I put this code in, the performance was along these lines:

    [info] 80% Scenario{vm=java, trial=0, benchmark=UnsafeUpdate} 7100.00 ns; σ=37.14 ns @ 10 trials
    [info] 90% Scenario{vm=java, trial=0, benchmark=UnsafeUpdateStride4} 7100.00 ns; σ=49.21 ns @ 10 trials

The first benchmark represents a `DenseVector` with `offset=0` and `stride=1`, while the second has `stride=4`. My hope was to see a speedup along the following lines:

    [info] 80% Scenario{vm=java, trial=0, benchmark=UnsafeUpdate} 4100.00 ns; σ=37.14 ns @ 10 trials
    [info] 90% Scenario{vm=java, trial=0, benchmark=UnsafeUpdateStride4} 7100.00 ns; σ=49.21 ns @ 10 trials

# WTF is going on?

This is what actually happened:

    [info] 80% Scenario{vm=java, trial=0, benchmark=UnsafeUpdate} 4097.48 ns; σ=37.14 ns @ 3 trials
    [info] 90% Scenario{vm=java, trial=0, benchmark=UnsafeUpdateStride4} 4071.90 ns; σ=49.21 ns @ 10 trials

**Both** strided and strideless array access sped up.

My first thought was that something about embedding the function in a `val` caused the speedup, since the speedup is clearly NOT caused by avoiding the `offset+i*stride` computation. So I tried this:

    private val innerUpdate: ((Int,E) => Unit) = if ((offset == 0) && (stride == 1)) { (i:Int,v:E) => {data(i) = v} } else {(i:Int,v:E) => {data(offset+i*stride)=v}  }

    def unsafeUpdate(i: Int, v: E) = innerUpdate(i,v)

Performance slowed back down to 7.1 microseconds.

Apparently the if-statement is necessary even though both versions of the code achieve the same performance.

To confuse things further, the `DenseVector` object also has a method `valueAt` which is used to retrieve a value. Using this same technique on `unsafeValueAt` did *NOT* result in a speedup.

## Any ideas?

So here comes the bleg. Does anyone have a clue what the fuck is going on?

The best I can guess is that the if-statement triggers some strange (and fragile) JVM optimization. Most likely this results in better inlining of the update code. But it's not just a matter of simple inlining, because this code takes 7 microseconds, not 4:

    @inline
    def unsafeUpdate(i: Int, v: E): Unit = { data(offset + i * stride) = v }

If anyone knows what is going on, I'd love to hear a good explanation.
