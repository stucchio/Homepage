title: Scala Patterns - HasXIsX
date: 2013-11-29 08:45
author: Chris Stucchio
tags: scala, design patterns





It's often desirable to build wrappers around existing objects, implementing the same interface. As an example one can wrap a `java.sql.Connection` object with a wrapper that measures timing data (how long the underlying `java.sql.Connection` spent in blocking calls). In fact, it's often useful to build a *sequence of wrappers*, each wrapper handling one specific layer of functionality. In the normal Java paradigm, this involves a lot of duplicate code - each method must be reimplemented at each wrapper layer.

Another place where code is often duplicated is when building compound objects that inherit from multiple traits. Consider a `VideoAdvertisement` class which must implement an `AdvertisementLike` interface - it's useful to build a constructor for `VideoAdvertisement` which takes `(Advertisement, Video)` as arguments, and most of the constructor will simply copy fields from `Advertisement` onto `VideoAdvertisement`.

Enter the `HasXIsX` pattern.



Consider an underlying `AdvertisementLike` trait:

    trait AdvertisementLike {
      def advertiser: Advertiser
      def campaign: Campaign
      def target: URL
    }

Now consider the `VideoAdvertisement`:

    case class VideoAdvertisement(advertiser: Advertiser, campaign: Campaign, target: URL, video: Video)
           extends AdvertisementLike

Depending on how the data storage layer is set up, we probably need to build a constructor like this:

    object VideoAdvertisement {
      def apply(advertisement: AdvertisementLike, video: Video) =
        new VideoAdvertisement(advertisement.advertiser, advertisement.campaign, advertisement.target, video)
    }

A lot of redundant code is created if we have multiple advertisement types - `FlashAdvertisement`, `PopupAdvertisement`, etc. The `HasXIsX` pattern can solve this:

    trait HasAdvertisementIsAdvertisement extends AdvertisementLike {
      protected val advertisement: AdvertisementLike
      def advertiser: Advertiser = advertisement.advertiser
      def campaign: Campaign = advertisement.campaig
      def target: URL = advertisement.target
    }

Then we redefine `VideoAdvertisement` as follows:

    case class VideoAdvertisement(advertisement: AdvertisementLike, video: Video)
           extends HasAdvertisementIsAdvertisement

If we similarly had a `HasVideoIsVideo` trait, it would be very easy for `VideoAdvertisement` to be both an `AdvertisementLike` and a `VideoLike`.

This method is also very handy for building wrappers. For example, I build a [ConnectionWrapper](https://github.com/stucchio/Tiramisu/blob/master/src/main/scala/tiramisu/utils/wrappers/ConnectionWrapper.scala) class in my [Tiramisu](https://github.com/stucchio/Tiramisu) SQL library:

    trait ConnectionWrapper extends java.sql.Connection {
      protected val conn: java.sql.Connection

      protected def methodWrap[T](f: =>T): T = f
      ...etc...

      def abort(x: java.util.concurrent.Executor): Unit = methodWrap { conn.abort(x) }
      def close(): Unit = methodWrap { conn.close() }
      def commit(): Unit = methodWrap { conn.commit() }

      protected def wrapPreparedStatement(stmt: java.sql.PreparedStatement) = stmt
      def prepareStatement(x: String): java.sql.PreparedStatement =
        wrapPreparedStatement(methodWrap { conn.prepareStatement(x) })

      ...etc...
      }

This saves me the trouble of re-wrapping every method when I build the `TimingSqlConnection` class:

    class TimingSqlConnection(protected val conn: java.sql.Connection) extends ConnectionWrapper {

      //new functionality
      def getTime: Long = timeCounter.get

      private def time[T](f: =>T): T = {...timing code...}

      override protected def methodWrap[T](f: =>T): T = time(f)

      protected case class TimingPreparedStatement(protected val stmt: java.sql.PreparedStatement) extends PreparedStatementWrapper {
        override def methodWrap[T](f: =>T): T = time(f)
        override def wrapResultSet(rs: java.sql.ResultSet) = TimingResultSet(rs)
      }

      override protected def wrapPreparedStatement(stmt: java.sql.PreparedStatement) = TimingPreparedStatement(stmt)
      ...etc...
    }

I.e., I get to avoid manually writing:

    def close(): Unit = time(conn.close())
    def commit(): Unit = time(conn.commit())
    ...repeat for every method

Take a look at the [utils](https://github.com/stucchio/Tiramisu/tree/master/src/main/scala/tiramisu/utils) folder of the Tiramisu repo, where I use this pattern to build a couple of handy wrappers.

Anyway, this is just a simple pattern I've found to save me a lot of code. Nothing groundbreaking, just a nice little use of scala traits.
