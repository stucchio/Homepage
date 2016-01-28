title: Free Monads in Scalaz - how to use them
date: 2015-06-22 09:00
author: Chris Stucchio
tags: scala, free monad, category theory, scalaz
category: category theory

In category theory, a Free Object is an algebraic object `M[_]` possessing a natural transformation - a way of lifting a function `f: A => N` into a function from `M[A] => N` which preserves the algebraic structure. In this article I'm going to discuss how this applies to the Free Monad and show how it can be used to compose database operations into transactions - an inherently monadic task.

There are several existing free monad tutorials out there on the net. Most of them start from implementation details and work their way back into explaining category theory and what a free monad is. I'm going to do the opposite, and start from category theory - i.e., the API for free monad - and simply explain how they are used. I'll leave implementation details to [other posts](http://noelwelsh.com/programming/2015/04/13/free-monads-are-simple/).

# The problem

Database transactions are an inherently monadic set of actions. We can do two things - run a query, and we can also update data. We want to ensure that these actions happen consistently using database transactions. Typical code might look like:

```scala
val conn = bonecp.getConnection()
conn.setReadOnly(false)
conn.setAutoCommit(false)
conn.rollback()
try {
  f(conn)
  val x = g(conn)
  h(x, conn)
  conn.commit()
} catch {
  case (e:Exception) => conn.rollback()
} finally {
  conn.close()
}
```

Unfortunately code like this is often difficult to compose. There is also a lot of boilerplate here. Is it possible to separate the individual functions (`f`, `g` and `h`) from the boilerplate?

One way to merge actions together is with a monadic structure. It's possible to define a completely new monad explicitly that will handle such things. But another way to handle such things is with Scalaz's [free monad](https://github.com/scalaz/scalaz/blob/scalaz-seven/core/src/main/scala/scalaz/Free.scala).

# The Free Monad

Let `S[_]` be any `Functor`. A Free Monad is any monadic type `T[A] = Free[S[_],A]` satisfying the following property: for any Monad `M[_]`, and any function `f: S[A] => M[B]`, there is a function `g: Free[S,A] => M[B]` with the property that `g(s.point[Free[S,A]]) = f(s)`.

In short, take any Functor `S[_]`. Then you can build a Monad out of it, and the monad is actually such a relaxed monad that you can map this monad into *any other monad*. This is in many ways a form of late binding - you can define monadic actions now, and worry about how to interpret them later.

# Database Transactions - the Monad

Now lets consider an example of how we would implement this. Defining a Free Monad is very easy. Lets start with a Functor:

```scala
case class SqlOp[A](act: Connection => A)
implicit object SqlOpFunctor extends Functor[SqlOp] {
  def map[A,B](a: SqlOp[A])(g: A => B) = SqlOp[B]((c:Connection) => g(a.act(c)))
}
```

We can now define the Free Monad based on this Functor:

```scala
type Sql[A] = Free[SqlOp,A]
```

We can define individual SQL operations as methods with the `Free.liftF: S[A] => Free[S,A]` function:

```scala
def markAccountAsUpdated(account: Account, when: DateTime): Sql[Boolean] = Free.liftF(
  SqlOp((conn:java.sql.Connection) => {
    conn.doStuff... // No calls to conn.commit() should live here.
    ...
  })
```

Once we have these database operations, we can combine them into a transaction we wish to run:

```scala
def getAccountAndMarkAccess(personId: Long): Sql[Account] = for {
  person <- getPerson(personId)
  account <- getAccount(person.accountId)
  _ <- if (account.auditingIsEnabled) { markAccountAsUpdated(account, DateTime.now()) } else { None }
  } yield (account)
```

If we call the function `getAccountAndMarkAccess(5)`, *no database actions are run*. Rather, a set of database actions to be run are defined. There is no need for any of these actions to contain a `conn.commit()` call - that is explicitly NOT the responsibility of the `SqlOp`.

Now if we want to actually *execute* the SQL operations, we need to build an interpreter. This can be done with the FreeMonad's `fold` operation:

```scala
def runTransactionImpl[A](conn: java.sql.Connection, trans: Sql[A]): A = trans.fold(
  (a:A) => a,
  (x:SqlOp[Sql[A]]) => runTransactionImpl(conn, x.act(conn))
)
```

In essence, the fold function is handling the evaluation of the monad. The first argument to `fold` explains how to handle `point`, while the second component is handling `bind`. To build the complete interpreter, one then need only deal with handling connections and the transaction itself:

```scala
def runTransaction[A](trans: Sql[A]): Exception \/ A = {
    val conn = bonecp.getConnection()
    try {
      val result: A = runTransactionImpl(conn, trans)
      conn.commit()
      result.right[Exception]
    } catch {
      case (e:Exception) => {
        conn.rollback()
        e.left[A]
      }
    } finally {
      conn.close()
    }
  }
```

We've now separated the implementation of the monad from it's execution. In fact, if we wanted, we could have multiple different ways of handling transactions - we would simply build different `runTransaction` and `runTransactionImpl` functions.

# Increasing testability

In a recent article, Jessitron discussed an [ultratestable coding style](http://blog.jessitron.com/2015/06/ultratestable-coding-style.html). In diagrams, she emphasized making IO and other such effects very simple, and focusing unit tests on the business logic portion of the code. I.e.:

```
val inputs = loadInputsFromDisk()

val inputsParsed = parseInputs(inputs)
val outputs = computeOutputs(inputsParsed)
val outputWriteActions = computeOutputWriteActions(outputs)

writeOutputs(outputWriteActions)
```

Every line except the first and last is easily unit tested - the first and last are of course potentially slow, due to the inherent limitations of disk or network. So Jessitron's goal was to minimize the amount of code not available under test, make that code as simple as possible, and test the rest aggressively. This is a great way to run tests to ensure things like, e.g., files are not written to a directory before the directory is created.

The only problem with this style is it doesn't always work. There are many cases where `outputWriteActions` would be too large to store in memory. For example, suppose the input is large but sparse. One might want to read a small subset of the data, but this could only be determined inside the `computeOutputs` function.

Another way to build a similar architecture is to use a `Free` monad to define the input/output actions one wishes to take - e.g., `ReadFile(file, offset, size)` or `MkDir(file)`. One would then build one evaluator `Free[FileActions,A] => IO[A]` to handle actually performing these actions and use a different evaluator `Free[FileACtions,A] => State[List[FileAction],A]` to handle running tests and checking which IO actions are performed.

The functor `S[_]` might then be:

```scala
sealed trait FileActionOp[A]
case class Pure[A](x: A) extends FileActionOp[A]
case class MakeDir[A](d: File, x: A) extends FileActionOp[A]
case class CreateFile[A](d: File, x: A) extends FileActionOp[A]

object F extends Functor[FileActionOp] {
  def map[A,B](fa: =>FileActionOp[A])(f: A => B) = fa match {
    case Pure(x) => Pure(f(x))
    case MakeDir(d,x) => MakeDir(d, f(x))
    case CreateFile(d,x) => CreateFile(d, f(x))
  }
}
```

The monad would then be:
```scala
type FileAction[A] = Free[FileActionOp,A]
```

Then to test whether a directory is always created before files are placed in it:

```scala
test {
  val result = for {
    d <- makeTempDir
    .....
    f <- Free.liftF(CreateFile(filename))
  } yield ()

  testEvalActions(result) match { //There are better ways to check if a file is in a directory
    case List(MakeDir(d, None), CreateFile(f, None)) if (f.toString.startsWith(d)) => true
    case _ => false
  }
}
```

where

```scala
def testEvalActions[A](f: Free[FileActionOp,A]): List[FileActionOp] = f.fold(
    (a:A) => List(),
    (x:FileActionOp[FileAction[A]]) => x match {
      case Pure(x) => testEvalActions(x)
      case MakeDir(d,x) => MakeDir(d,None) :: testEvalActions(x)
      case CreateFile(d,x) => CreateFile(d,None) :: testEvalActions(x)
    }
  ).reverse
```

(Reversal is necessary since we are prepending the last action to the list.)

In contrast, the non-testing implementation would actually create directories and files rather than merely prepending the desire to create them to a list.

This manner of structuring a program allows us to circumvent Jessitron's artificial limitations in which we must first read, then process, then write.
