title: How to return an array of generic type, or "cannot find class tag for element type T"
date: 2014-06-28 18:00
author: Chris Stucchio
tags: scala, classtag, covariance

I was recently writing some Scala code, and I wanted to return an array of generic type:


```scala
class Foo[+T] {
  def someArray(size: Int): Array[T] = {
    val result = new Array[T](size)
    ...
    result
  }
}
```

This did not make Scala happy:

    [info] Compiling 1 Scala source to /home/stucchio/src/breeze/math/target/scala-2.11/classes...
    [error] /home/stucchio/src/breeze/math/src/main/scala/breeze/stats/distributions/Rand.scala:66: cannot find class tag for element type T
    [error]     val result = new Array[T](size)

The standard solution to this is simply to pass an implicit classtag argument:

```scala
class Foo[+T] {
  def someArray(size: Int)(implicit m: ClassTag[T]): Array[T] = {
    val result = new Array[T](size)
    ...
    result
  }
}
```

Unfortunately, due to the `+T` in the class definition, that won't work:

    [info] Compiling 1 Scala source to /home/stucchio/src/breeze/math/target/scala-2.11/classes...
    [error] /home/stucchio/src/breeze/math/src/main/scala/breeze/stats/distributions/Rand.scala:65: covariant type T occurs in invariant position in type (size: Int)(implicit m: scala.reflect.ClassTag[T])Array[T] of method someArray

The problem here is the covariance - the `Array[T]` class is invariant in `T`. If we were allowed to do this, the following could happen:

```scala
val intFoo = new Foo[Int]
val anyFoo : Foo[Any] = intFoo

val anyArr : Array[Any] = anyFoo.someArray(1024)

anyArr(0) = intFoo //Throws runtime exception, since anyArr is (under the hood) an Array[Int]
```

The solution I found was to add an additional type parameter to the `someArray` method:

```scala
class Foo[+T] {
  def someArray[U >: T](size: Int)(implicit m: ClassTag[U]): Array[U] = {
    val result = new Array[U](size)
    ...
    result
  }
}
```

The net result:

    > (new Foo[Int]).someArray(1024)
    Array[Int] = Array(0,1,2,3, ...)
    > val r: Foo[Any] = new Foo[Int]
    > r.someArray(1024)
    Array[Any] = Array(0,1,2,3, ...)

This is of course the desired behavior.
