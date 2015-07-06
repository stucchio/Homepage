title: Preventing DB sharding errors at compile time with dependent types
date: 2015-07-06 09:00
author: Chris Stucchio
tags: scala, dependent types, databases
category: scala

Dependent types are a way of proving facts about your program at compile time. One interesting use case of dependent types, which I've discovered recently, is ensuring consistency in a sharded database system. [Sharding](https://en.wikipedia.org/wiki/Shard_(database_architecture)) is a database practice where different pieces of data are stored in different physical databases, depending on underlying properties of the objects.

Consider the following code:

```scala
def runDatabaseOperation[A](shard: Shard)(f: Connection => A): A = ...

case class User(username: String, shard: Shard)
case class BlogPost(content: String, shard: Shard)

def insertBlogPost(user: User, post: BlogPost) = runDatabaseOperation(user.shard)(conn => ...)
```

We'd like to ensure that each `BlogPost` is stored in the same `Shard` as the user who wrote it.

Unfortunately, problems can arise at runtime:

```scala
insertBlogPost(User("chris", Shard(1)), BlogPost("my blog post", Shard(2)))
```

This code cannot possibly run successfully, since the user lives in `Shard(1)` while the blogpost lives in `Shard(2)`.

If the underlying database is a SQL database, this will likely result in various consistency errors - the `BlogPost` will probably fail to be inserted, and further queries to `Shard(1)` of the form `SELECT ... FROM users INNER JOIN blogposts ON blogposts.user_id = user.id WHERE ...` will fail to return the blog post inserted into `Shard(2)`.

As a result, it is possible for bugs to occur that cannot be checked by the compiler.

# Class Hierarchies?

One possible way to handle this would be by creating a class hierarchy:

```scala
case class User(username: String, shard: Shard)
case class BlogPost(content: String, user: User) {
  def shard = user.shard
}

def insertBlogPost(post: BlogPost) = runDatabaseOperation(post.user.shard)(conn => ...)
```

This sort of hierarchical data structure can ensure that all posts have the same shard as the relevant user. But unfortunately this also imposes a fundamentally hierarchical model on the data itself - essentially, at least at the program level, we are giving up most of the benefits of a relational database.

# Dependent types to the rescue

I've recently discovered a way to use dependent types to ensure, at *compile time*, all data is inserted into the correct shard.

To begin, we define a datatype representing our shards:

```scala
case class Shard(id: Long) extends DBTypes
```

We then define a type to represent all the items that are associated to a shard:

```scala
trait HasShard {
  val shard: Shard
}
```

We then define various abstract types representing our data. For example:

```scala
trait UserLike extends HasShard {
  def username: String
}
trait BlogPostLike extends HasShard {
  def content: String
}
```

However, the concrete definitions of our data types live inside the `DBTypes` trait:

```scala
trait DBTypes { self:Shard =>
  trait HasMyShard extends HasShard {
    val shard: self.type = self
  }

  case class User(username: String) extends HasMyShard with UserLike
  case class BlogPost(content: String) extends HasMyShard with BlogPostLike
}
```

We define a `runDatabaseOperation` function which requires knowing the relevant shard:

```scala
def runDatabaseOperation[A](shard: Shard)(f: Connection => A): A = ...
```

Then, when we want to define functions taking datatypes, we do the following:

```scala
  def insertPost(user: UserLike)(post: user.shard.BlogPost) = insertIntoDB(user.shard)(...)
```

The type of the `Post` is now dependent on the *value* of `user.shard` - i.e., we are guaranteed at compile time that `user.shard === post.shard`. This means the following code will compile:

```scala
val s1 = Shard(1)
val u1 = s1.User("foo")
val p1 = s1.BlogPost("a foo post")
insertPost(u1)(p1)
```

But the following code will not:

```scala
val s1 = Shard(1)
val s2 = Shard(2)
val u1 = s1.User("foo")
val p2 = s2.BlogPost("a foo post")
insertPost(u1)(p2) //This line is an error
```
```
[error]  found   : s2.BlogPost
[error]  required: u1.shard.BlogPost
[error]   insertPost(u1)(p2)
```

## Chaining computations

To chain computations together, one must be careful to use type signatures which encode the information that is known about the result set. This would be the wrong way to do it:

```scala
  def getPosts(user: UserLike): List[BlogPostLike] = ...
```

Rather, what should be done is the following:

```scala
  def getPosts(user: UserLike): List[user.shard.BlogPost] = {
    ...
    val content: List[String] = ...database stuff...
    content.map(c => user.shard.BlogPost(c))
  }
```

This will ensure that the compiler knows the return type of `getPosts` lives in the same shard as `user`.

# Conclusion

Dependent types are a great way to encode facts about your program, and to ensure that these conditions are satisfied by your code. One common constraint is that all arguments to a function must be, in some way or another, associated to each other (e.g. they all come from the same DB shard). Scala's path-dependent types give us a great way to encode this type of constraint, and ensure data integrity at compile time.
