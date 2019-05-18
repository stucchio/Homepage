title: Don't use Hadoop - your data isn't that big
date: 2013-09-16 11:30
author: Chris Stucchio
tags: big data, buzzwords, hadoop
featured: true

![image possibly inspired by this post](/blog_media/2013/hadoop_hatred/oreilly.jpeg)


"So, how much experience do you have with Big Data and Hadoop?" they asked me. I told them that I use Hadoop all the time, but rarely for jobs larger than a few TB. I'm basically a big data neophite - I know the concepts, I've written code, but never at scale.

The next question they asked me. "Could you use Hadoop to do a simple group by and sum?" Of course I could, and I just told them I needed to see an example of the file format.

They handed me a flash drive with all 600MB of their data on it (not a sample, everything). For reasons I can't understand, they were unhappy when my solution involved `pandas.read_csv` rather than Hadoop.




Hadoop is limiting. Hadoop allows you to run one general computation, which I'll illustrate in pseudocode:

Scala-ish pseudocode:

    collection.flatMap( (k,v) => F(k,v) ).groupBy( _._1 ).map( _.reduce( (k,v) => G(k,v) ) )

SQL-ish pseudocode:

    SELECT G(...) FROM table GROUP BY F(...)

Or, as I [explained](../2011/mapreduce_explained.html) a couple of years ago:

>Goal: count the number of books in the library.
>
>Map: You count up the odd-numbered shelves, I count up the even numbered shelves. (The more people we get, the faster this part goes. )
>
>Reduce: We all get together and add up our individual counts.

The *only* thing you are permitted to touch is `F(k,v)` and `G(k,v)`, except of course for performance optimizations (usually not the fun kind!) at intermediate steps. Everything else is fixed.

It forces you to write every computation in terms of a map, a group by, and an aggregate, or perhaps a sequence of such computations. Running computations in this manner is a straightjacket, and many calculations are better suited to some other model. The only reason to put on this straightjacket is that by doing so, you can scale up to extremely large data sets. Most likely your data is orders of magnitude smaller.

But because "Hadoop" and "Big Data" are buzzwords, half the world wants to wear this straightjacket even if they don't need to.

## But my data is hundreds of megabytes! Excel won't load it.

Too big for Excel is not "Big Data". There are excellent tools out there - my favorite is [Pandas](http://pandas.pydata.org/) which is built on top of [Numpy](http://www.numpy.org/). You can load hundreds of megabytes into memory in an efficient vectorized format. On my 3 year old laptop, it takes numpy the blink of an eye to multiply 100,000,000 floating point numbers together. Matlab and R are also excellent tools.

Hundreds of megabytes is also typically amenable to a simple python script that reads your file line by line, processes it, and writes to another file.

### But my data is 10 gigabytes!

I just bought a new laptop. The [16GB of ram](http://www.amazon.com/gp/product/B0076W9Q5A/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B0076W9Q5A&linkCode=as2&tag=christuc-20) I put in cost me $141.98 and the 256gb SSD was $200 extra (preinstalled by Lenovo). Additionally, if you load a 10 GB csv file into [Pandas](http://pandas.pydata.org/), it will often be considerably smaller in memory - the result of storing the numerical string "17284932583" as a 4 or 8 byte integer, or storing "284572452.2435723" as an 8 byte double.

Worst case, you might actually have to not load everything into ram simultaneously.

### But my data is 100GB/500GB/1TB!

A [2 terabyte hard drive](http://www.amazon.com/gp/product/B005T3GRN2/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B005T3GRN2&linkCode=as2&tag=christuc-20) costs $94.99, [4 terabytes](http://www.amazon.com/gp/product/B005T3GRN2/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B005T3GRN2&linkCode=as2&tag=christuc-20) is $169.99. Buy one and stick it in a desktop computer or server. Then install [Postgres](http://www.postgresql.org/) on it.

## Hadoop << SQL, Python Scripts

In terms of expressing your computations, Hadoop is strictly inferior to SQL. There is no computation you can write in Hadoop which you cannot write more easily in either SQL, or with a simple Python script that scans your files.

 SQL is a straightforward query language with minimal leakage of abstractions, commonly used by business analysts as well as programmers. Queries in SQL are generally pretty simple. They are also usually very fast - if your database is properly indexed, multi-second queries will be uncommon.

Hadoop does not have any conception of indexing. Hadoop has only full table scans. Hadoop is full of leaky abstractions - at my last job I spent more time fighting with [java memory errors](/blog/2013/gc_overhead_limit.html), file fragmentation and cluster contention than I spent actually worrying about the mostly straightforward analysis I wanted to perform.

If your data is not structured like a SQL table (e.g., plain text, json blobs, binary blobs), it's generally speaking straightforward to write a small python or ruby script to process each row of your data. Store it in files, process each file, and move on. Under circumstances where SQL is a poor fit, Hadoop will be less annoying from a programming perspective. But it still provides no advantage over simply writing a Python script to read your data, process it, and dump it to disk.

In addition to being more difficult to code for, Hadoop will also nearly always be slower than the simpler alternatives. SQL queries can be made very fast by the judicious use of indexes - to compute a join, PostgreSQL will simply look at an index (if present) and look up the exact key that is needed. Hadoop requires a full table scan, followed by re-sorting the entire table. The sorting can be made faster by sharding across multiple machines, but on the other hand you are still required to stream data across multiple machines. In the case of processing binary blobs, Hadoop will require repeated trips to the namenode in order to find and process data. A simple python script will require repeated trips to the filesystem.

## But my data is more than 5TB!

Your life now sucks - you are stuck with Hadoop. You don't have many other choices (big servers with many hard drives might still be in play), and most of your other choices are considerably more expensive.

The only benefit to using Hadoop is scaling. If you have a single table containing many terabytes of data, Hadoop might be a good option for running full table scans on it. If you don't have such a table, avoid Hadoop like the plague. It isn't worth the hassle and you'll get results with less effort and in less time if you stick to traditional methods.


## P.S. Hadoop is a fine tool

I don't intend to hate on Hadoop. I use Hadoop regularly for jobs I probably couldn't easily handle with other tools. (Tip: I recommend using [Scalding](https://github.com/twitter/scalding) rather than Hive or Pig. Scalding lets you use Scala, which is a decent programming language, and makes it easy to write chained Hadoop jobs without hiding the fact that it really is mapreduce on the bottom.) Hadoop is a fine tool, it makes certain tradeoffs to target certain specific use cases. The only point I'm pushing here is to think carefully rather than just running **Hadoop** on **The Cloud**  in order to handle your 500mb of **Big Data** at an **Enterprise Scale**.

If you need help getting started with Hadoop, O'Reilly has a [decent](http://www.amazon.com/gp/product/1449311520/ref=as_li_ss_tl?ie=UTF8&amp;camp=1789&amp;creative=390957&amp;creativeASIN=1449311520&amp;linkCode=as2&amp;tag=christuc-20) (albeit slightly outdated) intro that will help you, only [$32 on amazon](http://www.amazon.com/gp/product/1449311520/ref=as_li_ss_tl?ie=UTF8&amp;camp=1789&amp;creative=390957&amp;creativeASIN=1449311520&amp;linkCode=as2&amp;tag=christuc-20).

*This article is also available [translated into Russian](http://habrahabr.ru/post/194434/).*
