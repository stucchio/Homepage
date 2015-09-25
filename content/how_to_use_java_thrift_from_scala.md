title: How to use Apache Thrift (Java version) from Scala
date: 2015-06-09 09:00
author: Chris Stucchio
tags: scala, apache thrift
category: apache thrift

There are a variety of methods of using [Apache Thrift](https://thrift.apache.org/) from Scala. [Scrooge](https://github.com/twitter/scrooge) from Twitter is a popular option, but it's only for Scala 2.9. That's a problem with most Thrift for Scala libraries - nothing is current for Scala 2.11. I've found the best way to get Thrift working from Scala is to simply use the Java/Thrift compiler, and then build an SBT task for that purpose. This blog post is just a quick howto on that.

To start with, you need the thrift compiler installed. I have thrift 9.0 installed, so I'll assume you are at least up to 9.

Once Thrift is installed, add the following to your `build.scala` file:

```scala
  lazy val buildThriftSettings = buildThrift := {
    import sys.process._
    Seq("thrift", "-o", "src/main/", "--gen", "java", "src/main/thrift/my_service.thrift")!

    Seq("thrift", "-o", "src/main/", "--gen", "java", "src/main/thrift/my_other_service.thrift")!
  }
```

This will build thrift Java sources in `src/main/gen-java`. That path should probably be added to your `.gitignore`.

The `buildThriftSettings` task should be added as a dependency on the project:

```scala
  lazy val myProject = Project("my_project", settings=myProjectSettings).settings(
    buildThriftSettings,
    buildThrift <<= buildThrift.triggeredBy(compile in Compile)
  )
```

Next one must tell SBT to look for java files in `src/main/gen-java`.

```scala
  lazy val myProjectSettings = Defaults.defaultSettings ++ Seq(
    ...all your settings...
    unmanagedSourceDirectories in Compile += baseDirectory.value / "src" / "main" / "gen-java",
    ...more of your settings...
  )
```

Finally, you need to add `"org.apache.thrift" % "libthrift" % "0.9.1" % "compile"` to your library dependencies.

That's all there is to it. Now my Thrift files are automatically compiled, accessible from Scala, and I don't need to worry about Scala dependency hell.
