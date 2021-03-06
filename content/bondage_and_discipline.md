title: Scala Compilation Speed - Bondage and Discipline will make you compile more quickly
date: 2014-01-30 08:30
author: Chris Stucchio
tags: scala, type systems, compilation speed, traits
nolinkback: true





Feeling stuck in a rut? Does programming make you feel bored, staring at the ceiling, waiting for your code to compile? I was in that place too. But over time, I've learned a few tricks to spice up my life and make my code compile faster. But it's not just compilation - when I made this change, I also discovered that my code become a lot cleaner and easier to work with. Dependency injection became easy and refactoring was a breeze.

Static type systems are often criticized as Bondage & Discipline programming, in contrast to the more flexible type systems of Python/Clojure/etc. But once I tried it out, I discovered I liked it. And you might too.




Before I continue, let me emphasize that my focus is on *incremental* compilation speed. This is how long it takes SBT to recompile when you have `~ compile` running in a console, and in my view this is what makes compilation feel slow. A large codebase will take you multiple minutes to compile from start to finish, but this will rarely slow you down when developing. In contrast, if recompiling takes 2 minutes after you edited 1 line of code, that will slow you down.

# How SBT recompilation works

The incremental compiler that ships with SBT is not as smart as it should be. Near as I can tell (note: I haven't looked at SBT's codebase, this is by observation), a request for recompilation is triggered whenever a file is changed. So if you change a file, the file will need to be recompiled. This cannot be escaped.

However, if you change an *interface*, a lot more needs to be recompiled. In principle, if you change a public method type signature, any class which uses that definition must be recompiled. In practice SBT is not smart enough to do that - if you change a public method type signature, then *any class which uses the class you changed* will be recompiled.

So for example:

    class G(x: String)
    class G2(val x: String, val y: Int) extends G(x)
    class G3(val x: String) extends G(x)

    class Foo {
      def f(x: String) = x.size*(x.size-1)
      def g(x: String) = new G2(x, x.size)
    }

In a separate file:

    object User {
      val foo: Foo = new Foo
      def h(x) = foo.g(x)
    }

## Changing a type signature

Consider an alteration:

    -  def f(x: String) = x.size*(x.size-1)
    +  def f(x: String) = (x.size*(x.size-1)).toLong

We've changed the type signature of `f` from `String => Int` to `String => Long`. Now the file containing `User` must be recompiled.

## Changing a type signature, part deux

Now consider a slightly different variation:

    -  def g(x: String) = new G2(x, x.size)
    +  def g(x: String) = new G3(x)

This will again change the type signature of `g` from `String => G2` to `String => G3`. However, it's quite possible that `User` doesn't much care about whether a `G2` or `G3` is returned - `User` may only care that a `G` is returned. Doesn't matter - recompilation is required.

# Cover your privates

My first big scala project was a large Play application. It was the first Scala project for approximately half the developers, most of whom were refugees (forced migrants?) from the world of Ruby on Rails. The culture of Ruby on Rails hipsters seems to be quite open - go ahead and monkeypatch `String`, it's all good.

Scala frowns on this.

    object FooDatabaseMethods {
      val baseFooQuery = "SELECT id, slug, title, size FROM foo "

      def getFoo(fooId: FooId) = {
        val query = baseFooQuery + " WHERE id=?"
        ...
      }
    }

Coming from a Java/Haskell/C++ background, I was blushing like a Mormon schoolgirl sending private tweets to Anthony Weiner.

As you might expect from the above discussion, simply adding another helper method (or changing implementation and removing one)

    val fooAndBarJoins = " INNER JOIN bar ON foo.bar_id = bar.id "

would force recompilation of the entire project, or at least every file that referenced `FooDatabaseMethods`.

I made one big change all over the codebase:

    -  val baseFooQuery = "SELECT id, slug, title, size FROM foo "
    -  private val baseFooQuery = "SELECT id, slug, title, size FROM foo "

All of a sudden small tweaks to implementation stopped forcing recompilation of the entire project. They also made refactoring and cleanup easier - if you alter a private method, you need only verify that the current class is correct. You don't need to worry that `baseFooQuery` was used by someone else somewhere in the project.

# Fluffy Handcuffs constrain your choices but don't cut off circulation

One of the big advantages to dynamic languages like Python or Ruby over old school statically typed languages (C++, Java) is that the rigid class heirarchies of the statically typed languages behaved like unpleasant metal handcuffs. A lot of changes which should be simple were made far more difficult by the compiler - you can't change the definition where you want to, you need to change it elsewhere in the class heirarchy.

In contrast, in Haskell and Scala, typing and class heirarchies are somewhat orthogonal. Typeclasses and Traits allow you to alter your types without using inheritance at all. I'm using the term fluffy handcuffs to describe such systems - they constrain your choices while hurting you a lot less in the process.

## Explicit Type Signatures

The first thing we can do is make our assumptions explicit.

    class Foo {
      def f(x: String) = x.size*(x.size-1)
      def g(x: String): G = new G2(x, x.size)
    }

Now the public interface of `Foo` specifies that the method `g` returns a `G` object. As a result, swapping out the `G2` for a `G3` will no longer force a recompilation of `User`.

This choice also constraints the actions of `Foo` users who are no longer permitted to make assumptions as to whether a `G`, `G2` or `G3` are returned. In my view this is a good thing - we've separate interface from implementation. We've also avoided an unpleasant pitfall - down the road, users of `Foo` might assume that both the fields `x` and `y` are available. If we swap out a `G2` for a `G3`, we would need to fix all this client code.

### Communicate your boundaries

Even in Haskell, where this is far less necessary for compilation speed, my code is often littered with type signatures. I find them helpful because they make it easier for me to figure out what is happening - I don't need to read a function definition to understand what type it returns.

They also provide a useful check: are the compiler and I really on the same page? It happens to the best of us - sometimes there is a misunderstanding between me and the compiler. I believe I'm returning a `Set[MyType]`, it thinks I'm returning a `Seq[MyType]`. Or worse, it warns me that I'm actually returning an `Any`.

Most of the time my type signatures are just wasted bytes. But I'm sure glad to waste the bytes on those rare occasions when the compiler and I are not on the same page.

**Side note:** in at least Scala 2.9, there is a compiler bug that will sometimes prevent proper inference of return types. I've discovered this to happen sporadically (I can't always reproduce it) and it typically involves code of the form:

    def f(x: Int) = if (x % 2 == 0) {
        new Foo with MyTrait
      } else {
        new Bar with MyTrait
      }

Since `Foo` and `Bar` have only `Any` as a common ancestor, the compiler will sometimes return an `Any`. In contrast, changing this to `def f(x: Int): MyTrait` works perfectly.

## Composition of traits

It turns out that `Foo` has some relatively orthogonal methods. It's `f` method is used for computing a measure of the size of a string, whereas it's `g` method is used for constructing `G` objects. There may be some good reason for providing them both on the same object, but not all client code needs to know about this. We can exploit this:

    trait GFactory {
      def g(x: String): G
    }

    class Foo extends GFactory {
      ...details unchanged...
    }

Elsewhere:

    object User {
      val gFactory: GFactory = new Foo
      def h(x) = foo.g(x)
    }

Now suppose we alter the type signature of `f` but leave `g` unchanged. We will no longer need to recompile `User`. This is because the `User` object doesn't know it has a `Foo` - all it knows is it has a `GFactory`.

### Easy Dependency Injection

In addition to speeding up incremental compilation, we've made our life easier in another way. If we want to test `User`, we can separate out the `User` functionality from the `Foo` functionality. All we need to do is build a `MockGFactory extends GFactory` and inject it into `User`. We do not need to not need to build a mock implementation for all of `Foo`.

Similarly, swapping out the implementation of `GFactory` for `User` has been made easier as well.

## Compose traits for value types

Consider the case class:

    case class UserFull(name: String, email: String, address: String, geo: GeoLocation, ..., 15 other fields)

You've got a common method `getUser` which returns `User` objects that are processed in many locations. But many of the functions that *use* the value type don't need all those fields. You can often write more general code by breaking things up:

    trait UserLike {
      def name: String
      def email: String
    }

    trait HasAddress {
      def address: String
      def geo: GeoLocation
    }

    case class User(name: String, email: String, address: String, geo: GeoLocation, ..., 15 other fields) extends UserLike with HasAddress

Downstream methods can then specify the functionality they need:

    def sendEmail(u: UserLike) = ...
    def showOnMap(g: HasAddress) = ...

Adding a new field to the `User` class will no longer force all the utility methods to be recompiled.

This decomposition also makes your code more functional. If `showOnMap` took a `User`, it could only be used for `User` objects. Since it takes only a `HasAddress` method, it works on `class Business(...) extends HasAddress` as well.

# Extend with Typeclasses

Suppose you had a bunch of objects which need to be serialized:

    case class User(name: String, ...) extends JsonSerializable {
      def toJson: Json = {...}
    }

    case class Address(streetName: Street, ...) extends JsonSerializable {
      def toJson: Json = {...}
    }

    ...

Now at some point, you have a widely used class `GeoLocation` which suddenly needs to be serialized.

    - case class GeoLocation(lat: Long, lon: Long)
    + case class GeoLocation(lat: Long, lon: Long) extends JsonSerializable {
      def toJson: Json = {...}
    }

You've just altered the public method signature of a class which could be used in hundreds of locations. Massive recompile needed.

On the other hand, if you used typeclasses for json serialization (see, e.g. [Spray Json]()), this would not be the case. You'd simply create a typeclass:

      object JsonSerializers extends DefaultJsonProtocol with SprayJsonSupport {
         ...
    +    implicit val GeoLocationFormatter = jsonFormat2(GeoLocation.apply)
      }

This requires no recompilation.

**Warning:** It's worth noting the tradeoff here between *total* compilation speed and *incremental* recompilation speed. The former will probably go up if you use a lot of complicated typeclasses even if the latter will go down.

# Minimize the scope of implicits

Implicit resolution is another major source of slowness, particularly for complicated type signatures. It's also a major source of complication for other people trying to understand your code.

I've found that implicits are best used locally, and in places where their scope is obvious:

    def getFoo(fooId: Long)(implicit connection: java.sql.Connection) {
      ...SQL library finds implicit connection...
    }

I'm generally a big fan of Python's approach - explicit is better than implicit. Scala implicits are occasionally useful, particularly when used in moderation.

Unfortunately the most popular libraries (Akka and Scalaz) are big culprits in overuse of implicits. So while it's good to avoid them, it's not always possible.

# Smaller is better

This one goes without saying, but nevertheless I often avoid it. The less code you have, the less time it will take to compile. Be liberal about deleting code. If it isn't used, and won't be used in the immediate future, kill it - it's only slowing you down. It's always a good exercise to delete code and see if everything compiles just fine without it. If it does, you probably didn't need it.

Deleted code is also very easy to maintain.

# Slow compilation is a spanking for a bad boy

The Scala compiler is slow, make no mistake. Combining wanna-be Haskell style type inference with Java style subtyping and type erasure and you get, well, a lot of work for the compiler. Resolving implicits only makes things worse. (You also get a lot of work for the developers forced to fight with all this complexity.)

Speeding up the compiler is a very important project (perhaps the #2, after simplifying collections) and the scala world needs to improve it. But at the same time, a lot of the slow compilation issues are justa result of the compiler finding it difficult to figure out code which is overcomplicated. Every time I perform a major simplification, I find that the compiler becomes noticeably faster. So if your code is slow to compile/recompile, treat that as a code smell. If it takes the compiler 20 seconds to figure out your code, think about how long it will take you or your fellow developers to do the same.
