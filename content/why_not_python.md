title: Why Not Python - the GIL hinders concurrency
date: 2013-07-02 08:00
author: Chris Stucchio
tags: algorithms, python, concurrency





Python is not ready for the big leagues, at least if you need to deal with concurrency. I know this is a fairly controversial statement, and I plan to back it up with very specific critiques. The general gist of my critique is that python fails to properly utilize modern multicore hardware under concurrent situations. Instead, Python forces you to manually build a distributed system and then deploy it to a single box. This is true even for jobs which do not need to be distributed, and could easily be run on a single box.

In this post I plan to show why this is a problem and describe how other languages address these issues with lower CPU and memory consumption.




Before I get into my critiques, let me give my background. I've been using Python in scientific computing since about 2005, where I found it to be a vastly superior alternative to C++. My parallelism issues at that time were solved by using a shared memory array (in Numarray, a precursor to Numpy) and unix signals to notify forked processes when to run an FFT on the shared memory array. All of my past startups were built on a Python/Django stack, typically using Numpy for the scientific components. Most recently, I started a new work project in Python last week.

I'm not attempting to engage in some language holy war, I'm simply describing one concrete drawbacks of using Python for certain use cases - specifically, soft realtime event processing. Examples of problems in this space include high frequency trading and a website monitoring/optimization system. My critique applies not only to Python, but also to any other single threaded language relying on multiprocessing for concurrency and parallelism (including Javascript, Ruby and OCaml). I simply choose to pick on Python since I use it heavily.

The [GIL](http://dabeaz.com/python/UnderstandingGIL.pdf) is a problem. It's not a big issue in Python's primary niches (web development and scientific computing), but it is a problem in other areas. And if you use Python to build such a system, you will likely have to suffer the slings and arrows of distributed computing far earlier than necessary, all the while wasting CPU cycles and memory.

## Fanout message passing

Consider a market containing 4 securities - AAPL, GOOG, BP and XOM. To trade based on these securities, you want to track 4 types of statistics:

- Per-security statistics - e.g., the bid/ask spread of AAPL.
- Per-sector statistics, such as the volatility of tech (AAPL, GOOG) or the volatility of oil (BP, XOM).
- Global statistics, such as the S&P 500 (a weighted sum of the share prices of various individual securities).

You will typically then have one or more processes monitoring these statistics, and submitting orders to the market based on them. Doing this in parallel is ideal - you don't want the statistics on GOOG to be delayed simply because something is slowing down the per-sector statistics.

(For information on the details of algorithmic market making, go read my [previous](http://www.chrisstucchio.com/blog/2012/hft_apology.html) [posts](http://www.chrisstucchio.com/blog/2012/hft_apology2.html) on the subject.)

This is the problem we wish to solve, so lets explore Python's approach to this.

In pythonic pseudocode, we want to do something like this:

    def process_quote_stream(statistics_process_queues):
        for fix_blob in fix_message_stream(broker_host, broker_port):
	    quote = deserialize_from_fix(fix_blob)
	    for q in statistics_process_queues:
                q.put(quote)


    def first_statistics_process(queue):
        while True:
	    quote = queue.get(block=True)
	    statistic += quote.some_value

    def second_statistics_process(queue):
        ...

Whenever a GOOG quote comes in, it must be distributed to the GOOG statistics collectors, the per-sector statistics collectors (e.g., volatility of tech) and the global statistics collectors.

### Multiprocessing in Python

The standard Python workaround to the GIL is [multiprocessing](http://docs.python.org/3/library/multiprocessing.html). Multiprocessing is basically a library which spins up a distributed system running locally - it forks your process, and runs workers in the forks. The parent process then communicates with the child processes via unix pipes, TCP, or some such method, allowing multiple cores to be used.

The typical method of doing this with python would be to spin up one process to listen to the incoming event stream. This process would then stream events to the appropriate listener processes (typically one per statistic) and they in turn stream the statistics to the decision maker processes. For this discussion I'll focus solely on the process where a single event comes in and is fanned out to the statistics processes.

1. The event (say in FIX/OUCH format) reaches the python listener process and is deserialized into a python data structure.
2. The listener process re-serializes the python data structure (into, e.g., a pickle) and transmits the serialized version to multiple statistics processes.
3. Each statistics process de-serializes back to the *exact same python data structure*, of which we now have many copies.
4. The listener garbage collects the data structure.
5. Each statistics process does work garbage collecting the data structure.

You can skip a few steps here by having the statistics processes listen to FIX and not deserialize the event in step 2 (thereby transmitting only a FIX message), but fundamentally you need to deserialize once per statistics process and have multiple copies of the event floating around in memory.

It's important to note that the serialization/deserialization step might be the most difficult part of this process - consider deserializing a json blob, followed by incrementing a counter based on some value inside it.

The net result is that your CPU does a lot of unnecessary work and your memory stores a lot of duplicated data.

### Shared Immutable Objects in Scala/Haskell/Java

In each of the aforementioned languages, you have threads which do not block on any sort of GIL. So rather than spinning up multiple processes, you will spin up multiple threads. You'll have a single listener thread, and each statistics process will have one thread as well. Or alternatively you might use lightweight threads (Haskell does this) or actors (see Akka) - this means that you write code as if you have a large number of threads, but the underlying architecture maps this down onto approximately `numThreads == numCpus`.

Then when an event enters the system, a single listener *thread* will deserialize it from FIX. The following occurs:

1. The event is deserialized into an immutable Haskell/Scala data structure.
2. The listener process transmits a pointer to this immutable data structure to the statistics threads.
3. Each statistics thread processes the same immutable data structure, which has a good chance at already being in the CPU cache from a previous statistics process.
4. One garbage collector eliminates it when everyone is finished.

With this approach, memory consumption is reduced by a factor of O(number of statistics threads). CPU load is reduced considerably since deserialization only needs to occur once. Latency is reduced because you don't need to repeatedly deserialize the same data, and further reduced because each thread is acting on the *same block of memory* - this helps with cache locality.

## Caching vs the Thundering Herds

Consider a pure function, `f(x)`, which is expensive to compute. Due to it's purity, caching it is a viable method of reducing the cost of computation. The simplest way to do this in python would simply be to use a function caching decorator, e.g. my `@lru_cache_function` from [pylrucache](http://github.com/stucchio/Python-LRU-cache):

    @lru_cache_function
    def f(x):
        ...body...
	return result

The code of `lru_cache_function` is roughly what you expect, module a few details:

    ...
    key = repr( (args, kwargs) ) + "#" + self.__name__
    try:
        return self.cache[key]
    except KeyError:
        value = self.function(*args, **kwargs)
        self.cache[key] = value
        return value

Whenever `f(x)` is called, the result is cached, and future results are pulled from the cache.

Now consider a forked web application (e.g., gunicorn), with perhaps 4-8 workers. The first problem is simply memory duplication - the cache is duplicated 4-8 times, and stores the same thing. The second problem is the thundering herds problem. Consider a new input to `f(x)`, which becomes available at time `t=0`. At time `t=0`, the application is hit with multiple requests for this input. As a result, *each process* blocks while computing `f(new input)`.

Memory duplication has a relatively simple solution, namely using external cache such as redis. But the thundering herds problem remains. At time `t=0`, each process receives a request for `f(new input)`. Each process looks in the cache, finds it empty, and begins computing `f(new input)`. As a result *every single process is blocked*. **Update** - I'm told that one can [build locks with redis](http://www.dr-josiah.com/2012/01/creating-lock-with-redis.html), so this might not be as difficult as I thought. I'm also told that [dogpile.cache](https://dogpilecache.readthedocs.org/en/latest/usage.html) provides this.

### The Scala Solution

In Scala, the excellent [Spray Caching](http://spray.io/documentation/1.2-M8/spray-caching/) library is available which resolves this problem. The basic idea of the Spray Cache (which makes use of threading concurrency) is to store not the value itself, but instead [Future](http://www.scala-lang.org/api/current/index.html#scala.concurrent.Future) which will eventually evaluate to it. The client code is basically as simple as the python equivalent:

    def f(x: KeyType) = cache(x) {
        ...body...
	}

Under the hood, the cache is implemented roughly like this:

    val fromCache = cache.get(key)
    if (fromCache != null) {
        return fromCache
    } else {
        val result = Future { // This block is run in a different thread!
	    ...body...
	    }
        cache.put(result)
	return result
    }

Unlike the python equivalent this block of code returns instantly. The actual `...body...` is not actually run in the current thread. The net result is that repeated calls to `f(x)` return the same `Future`, and the result of the computation is available to all callers of `f(x)` as soon as it is computed. I.e., suppose it takes 100ms to compute `f(x1)`. Suppose Thread A calls `f(x1)` at `t=0`, and Thread B calls `f(x1)` at `t=50`. Then the result of `f(x1)` (i.e., the same memory location, which hopefully refers to an immutable object) is available to both Thread A and Thread B at `t=100`.

One possible implementation of such a strategy in Python would be to not expose the external cache directly, but rather to hide it behind some API which would then push the result to clients when it has been computed. This is certainly possible to build, though of course you do suffer the serialization and memory duplication overhead described in the previous section. The implementation would also likely be considerably more complicated than the [160 lines of code](https://github.com/spray/spray/blob/master/spray-caching/src/main/scala/spray/caching/LruCache.scala) that the Spray Cache uses.

## Scripting vs Systems

Ultimately, Python is a single threaded scripting language. It excels at coordinating external systems which handle heavy lifting and concurrency on their own. As examples of external systems, consider a SQL database or simple scalar arrays (ala Numpy). If you use it for this purpose it will serve you well. But fundamentally, the GIL prevents Python from being used as a systems language. The restriction that a single OS process be fundamentally single threaded prevents you from properly making use of modern multicore hardware. For this reason Python will continue to be limited to the scripting role, and those who wish to make full use of their hardware will be forced to turn to alternatives (e.g. Go, Java, Haskell or Scala).
