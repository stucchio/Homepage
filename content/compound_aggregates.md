title: Compound Aggregates in Hadoop/Scalding
date: 2013-09-26 08:00
author: Chris Stucchio
tags: hadoop
mathjax: true





Consider the following problem. I have an extremely large number of servers, each of which uploads their logs to a Hadoop cluster. Each line of the log file contains a server IP address, and represents a single message in Hadoop. I'm investigating a network intrusion. One of my network admins has observed a set of odd log messages on September 9 on several servers, and he believes they may be connected to the intrusion.

I want to use Hadoop to make a post-hoc measurement. I have a reasonably accurate method of checking whether a server was compromised, specifically a certain line that appears in the logs.

Combining data across the two dates in [Scalding](https://github.com/twitter/scalding) is a problem that puzzled me for a little while. For this reason, I think it's worthwhile to write down the solution I came up with.




In order to find servers with the suspicious log messages on September 9, I would run a job of this nature:

    class IntrusionPostHocCheck(args: Args) extends Job(args) {
      TextLineMultiPath(filenames: _*).read
        .flatMap('line -> 'logMessage)( (line:String) => parseLogMessage(line))
        .map('logMessage -> 'serverId)((l:LogMessage) => l.serverId())
        .filter('logMessage)( (l:LogMessage) => isLogMessageSuspicious(l) )
        .groupBy('serverId)( g => g.size('messageCount) )
    }

This Scalding job will come up with a list of server ID's with suspicious messages on September 9, and count the number of log messages for those servers over all time.

I could run a separate job to check for intrusions, of the form:

    class IntrusionPostHocCheck(args: Args) extends Job(args) {
      TextLineMultiPath(filenames: _*).read
        .flatMap('line -> 'logMessage)((line:String) => parseLogMessage(line))
        .map('logMessage -> 'serverId){(l:LogMessage) => l.serverId()}
        .filter('intrusionDetected)( (l:LogMessage) => wasIntrusionDetected(l) )
        .groupBy('serverId)( g => g.size('messageCount) )
    }

Following which I could perform an inner join on the output of both these jobs. This will give me a list of servers for which both a suspicious log message was detected, and an intrusion detected. But this isn't what I really want.

What I really want to do is measure:

$$ P( \textrm{intrusion} | \textrm{suspicious log message} ) $$

and similarly

$$ P( \textrm{intrusion} | \textrm{no log message} ) $$

If $$ P( \textrm{intrusion} | \textrm{suspicious log message} ) \gg P( \textrm{intrusion} | \textrm{no log message} ) $$ then we have evidence that the suspicious log messages and the intrusion are closely connected. If the two numbers are roughly equal, we have discovered that the suspicious log message and intrusions are uncorrelated.

So we really want to write a job to compute these probabilities.

The fastest and simplest way I've found to do this is with a compound aggregate. Here is how it works:

    case class CompoundAggregate(var suspiciousLogMessage: Boolean, var intrusionDetected: Boolean)
            extends org.apache.hadoop.io.Writable {
        //mutability of the class is necessary since org.apache.hadoop.io.Writable interface is mutable
        def this() = this(false, false) //Needed by Hadoop

        def +(other: CompoundAggregate) =
	    CompoundAggregate(suspiciousLogMessage || other.suspiciousLogMessage,
	                      intrusionDetected || other.intrusionDetected)

        ...serialization, i.e. implementation of org.apache.hadoop.io.Writable goes here...
    }

The job then looks like this:

    class CorrelationBetweenIntrusionSuspiciousMessage(args: Args) extends Job(args) {
      TextLineMultiPath(filenames: _*).read
        .flatMap('line -> 'logMessage)( (line:String) => parseLogMessage(line))
        .map('logMessage -> 'serverId)((l:LogMessage) => l.serverId())
        .map('logMessage -> 'aggregate)((l:LogMessage) => CompoundAggregate( isLogMessageSuspicious(l), wasIntrusionDetected(l) ) )
        .groupBy('serverId)( g => g.reduce('agg)( (x:CompoundAggregate, y:CompoundAggregate) => x + y )
    }

The output is then a listing of tuples of the form `(serverId, (suspiciousLogMessage, intrusionDetected))`. From this correlations between suspicious log messages and intrusions can be computed, e.g.:

        .groupBy('agg)(g => g.count('serverCount) )

As an additional performance hack to avoid unnecessary object creation (i.e. to avoid [this nonsense](/blog/2013/gc_overhead_limit.html)), one can mutate the compound aggregate in the reduce step rather than creating new objects:

    case class CompoundAggregate(var suspiciousLogMessage: Boolean, var intrusionDetected: Boolean)
            extends org.apache.hadoop.io.Writable {
        ...

        def +=(other: CompoundAggregate) = {
            suspiciousLogMessage = suspiciousLogMessage || other.suspiciousLogMessage
            intrusionDetected = intrusionDetected || other.intrusionDetected
          }
        ...
    }

and then in the job:

    .groupBy('serverId)( g => g.reduce('agg)( (x:CompoundAggregate, y:CompoundAggregate) => {
        x += y
        x
      })

(Due to the way Hadoop recycles writables, `x` and `y` will not be garbage collected very often. But in the prior implementation, `x+y` would be garbage collected once for each invocation of the reduce.)
