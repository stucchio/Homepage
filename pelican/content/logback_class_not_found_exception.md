title: Logback error 'java.lang.ClassNotFoundException: org.codehaus.janino.ScriptEvaluator'
date: 2014-01-23 05:00
author: Chris Stucchio
tags: logback, logging, exception





Just a quick fix to a problem I ran into, putting it out there just in case it helps someone. Ignore this post if you haven't run into this exception.

While configuring logback in order to filter out a bunch of `redis.actors.RedisClientActor` messages (tangential note: rediscala WTF?) I ran into the following error:

    Failed to instantiate [ch.qos.logback.classic.LoggerContext]
    Reported exception:
    java.lang.NoClassDefFoundError: org/codehaus/janino/ScriptEvaluator
            at ch.qos.logback.core.boolex.JaninoEventEvaluatorBase.start(JaninoEventEvaluatorBase.java:57)
            at ch.qos.logback.core.joran.action.NestedComplexPropertyIA.end(NestedComplexPropertyIA.java:167)
            ...

            at scala.concurrent.forkjoin.ForkJoinPool.runWorker(ForkJoinPool.java:1979)
            at scala.concurrent.forkjoin.ForkJoinWorkerThread.run(ForkJoinWorkerThread.java:107)
    Caused by: java.lang.ClassNotFoundException: org.codehaus.janino.ScriptEvaluator
            at java.net.URLClassLoader$1.run(URLClassLoader.java:366)
            ...



Turns out that to use the `ch.qos.logback.core.filter.EvaluatorFilter` (which allows you to filter log messages by regex), you need to include the following dependency *in addition to logback*:

    "org.codehaus.janino" % "janino" % "2.6.1"

    <dependency>
        <groupId>janino</groupId>
        <artifactId>janino</artifactId>
        <version>2.5.10</version>
    </dependency>

(Take your pick whether you prefer sbt or maven.)

You can also suppress [rediscala](https://github.com/etaty/rediscala) log messages by putting:

    rediscala {
      loglevel = "ERROR"
    }

into your application.conf.

Just putting this on the interwebs in the hope someone finds it useful.
