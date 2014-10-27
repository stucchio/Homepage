title: NullPointerException when running distcp to Amazon s3 filesystem
date: 2011-04-12 00:00
author: Chris Stucchio
tags: development, apache thrift




I recently ran into the following error when trying to copy data from a local Hadoop cluster into Amazon S3:

    #!bash
    $ hadoop distcp -i / s3n://USERID:SECRETKEY@BUCKETNAME/
    11/04/13 07:15:31 INFO tools.DistCp: srcPaths=[/]
    11/04/13 07:15:31 INFO tools.DistCp: destPath=s3n://USERID:SECRETKEY@BUCKETNAME/
    With failures, global counters are inaccurate; consider running with -i
    Copy failed: java.lang.NullPointerException
    	at org.apache.hadoop.tools.DistCp.makeRelative(DistCp.java:901)
    	at org.apache.hadoop.tools.DistCp.setup(DistCp.java:1059)
    	at org.apache.hadoop.tools.DistCp.copy(DistCp.java:650)
    	at org.apache.hadoop.tools.DistCp.run(DistCp.java:857)
    	at org.apache.hadoop.util.ToolRunner.run(ToolRunner.java:65)
    	at org.apache.hadoop.util.ToolRunner.run(ToolRunner.java:79)
	at org.apache.hadoop.tools.DistCp.main(DistCp.java:884)



After some googling, I discovered that this turned out to be a [bug](https://issues.apache.org/jira/browse/MAPREDUCE-968?page=com.atlassian.jira.plugin.system.issuetabpanels%3Aall-tabpanel#issue-tabs) in Hadoop 0.20. A fix for Hadoop 0.21 is already submitted, but what do I do in the meantime?

It took quite a bit of puzzling, but I eventually figured out that this is only a bug in distcp. In particular, this bug does NOT apply to hadoop fs -cp. So we can solve this with a little command-line fu:

    #!bash
    for p in `hadoop dfs -ls / | cut -c 66-100`;
    do
        hadoop fs -cp $p s3n://USERID:SECRETKEY@BUCKETNAME$p;
    done;

