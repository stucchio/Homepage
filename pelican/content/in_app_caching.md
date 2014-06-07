title: In-app caching - spend a little RAM to speed up your site
date: 2012-04-07 10:00
author: Chris Stucchio
tags: django, caching





HTTP is a stateless protocol. For this reason, it's often considered bad practice to store data in your server's memory the memory of your webserver to be a bad practice. In general, this is correct - your webserver's ram is a bad place to store permanent data. It's volatile, and if you have multiple servers behind a load balancer, it's likely to give inconsistent results between requests.

But it's a great place to cache certain pieces of data.



Lets start with a fairly simple set of database models to use as an example:

    class Currency(models.Model):
        name = models.CharField(max_length=256)

    class Security(models.Model):
        name = models.CharField(max_length=256)
        currency = models.ForeignKey(Currency)

A naive way to create a view of the Security object is as follows:

    def security_view(request, security_id):
        security = Security.objects.get(id=int(security_id))
        return render_to_response("security_template.html", { 'security : security })

The template might look something like this:

    
    <div>
        <h1>{{security.name}}</h1>
        <h2>Currency {{security.currency.name}}</h2>
    </div>
    

This is not the fastest way to render the view. When the currency field is accessed inside the template, a second sql query is made to retrieve the currency object:

    SELECT "trading_security"."id", "trading_security"."name", "trading_security"."description",
           "trading_security"."currency_id" FROM "trading_security"
	   WHERE "trading_security"."id" = 142271

    SELECT "trading_currency"."id", "trading_currency"."name" FROM "trading_currency"
            WHERE "trading_currency"."id" = 136

In my setup (a couple of large instances on EC2), these two queries took 2-3ms each. There isn't much that we can do in the way of database optimization to speed this up - the network latency between these two boxes is 1.8ms:

    $ ping IP_ADDRESS
    PING IP_ADDRESS (IP_ADDRESS) 56(84) bytes of data.
    64 bytes from IP_ADDRESS: icmp_req=1 ttl=58 time=1.87 ms
    64 bytes from IP_ADDRESS: icmp_req=2 ttl=58 time=1.88 ms
    ...

In a page displaying many `Security` objects, this would be even worse. We might have a single SQL query to return a list of 50 `Security`s, together with 50 individual SQL queries to return each brand. That's at least 50ms of latency, wasted.

### select_related

Django has a built in solution for this - [select_related](https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related). The `select_related` method allows us to follow foreign keys in the query:

    def security_view(request, security_id):
        security = Security.objects.select_related('currency').get(id=int(security_id))
        return render_to_response("security_template.html", { 'security' : security })

The resulting SQL query retrieves both the security and the currency:

    SELECT "trading_security"."id", "trading_security"."name", "trading_security"."description",
           "trading_security"."currency_id", "trading_currency"."id", "trading_currency"."name"
           FROM "trading_security" LEFT OUTER JOIN "trading_currency" ON
                ("trading_security"."currency_id" = "trading_currency"."id")
	        WHERE "trading_security"."id" = 146076

This takes me 2-6ms to run, an improvement but not a big one. It is a considerably bigger improvement when accessing many `Security` objects simultaneously (e.g., `[ i.currency for i in Security.objects.all()[0:50] ]`) - the latencies involved in repeatedly querying for the currency definitely add up.

The biggest problem with `select_related` is that you need to constantly think about when and how to use it. Every time you write a view, you need to think - "do I need the currency field?" If you have many foreign keys on a given model, you need to specify which ones you want to follow or else the queries will return the contents of many unused fields.

Further, using it imposes a bit of a load on the database - it's always desirable to avoid joins, if you can get away with it.

## In-App Caching

One solution to many of these issues is in-app caching. There are two key issues which are necessary to make this a viable strategy:

* The amount of data to be cached cannot be large.
* The data should be frequently repeated.

So in our example of `Security` and `Currency`, the `Currency` field is a good candidate for in-app caching. There are tens of thousands of securities in the world, but only a few hundred currencies. (For the sake of argument, let's imagine that tens of thousands of securities would not easily fit into 512mb RAM.)

A simple way to do this would be to create a [memoized](https://en.wikipedia.org/wiki/Memoization) getter-function:

    @lru_cache_function(max_size=1024*8, expiration=60*60)
    def get_currency(id):
        return Currency.objects.get(id=id)

The decorator `lru_cache_function` is taken from [Python-LRU-cache](https://github.com/stucchio/Python-LRU-cache). It's basically just a [memoization](http://en.wikipedia.org/wiki/Memoization) decorator, but it handles cache expiration and makes sure the table of cached values doesn't become too large. In principle, you could probably just cache with a dict if you wanted.

Using this approach, we might want to build a `get_currency` method on `Security`:

    class Security(models.Model):
        name = models.CharField(max_length=256)
        description = models.TextField()
        currency = models.ForeignKey(Currency, related_name='securitys', null=True)

        def get_currency(self):
            return get_currency(self.currency_id)

The field `security.currency_id` represents the primary key of the Currency associated to the Security. When you access `security.currency`, django will transparently query the database to retrieve the currency. When you call `security.get_currency()`, it won't necessarily do this.

### Why not use memcached?

Another possible solution to this problem is to use memcached. We might define `get_currency(self)` as follows:

    def get_currency(self):
        result = cache.get(currency_by_id' + str(self.currency_id))
        if not result:
            result = Currency.objects.get(id=self.currency_id)
            cache.set(currency_by_id' + str(self.currency_id), result)
        return result

The problem with this approach is that it's not much faster than just querying the database. In a simple test measuring the time it takes to run `[ i.get_currency() for i in Security.objects.all()[0:50] ]` (each currency was already in the cache), I found that this approach took about 40ms to run. For comparison, `[i.currency for i in Security.objects.all()[0:50] ]` took about 50ms.

(I use nice round numbers to avoid the appearance of false precision - these numbers varied from moment to moment, presumably due to variations in network speed in EC2.)

The reason for this is network latency - it's impossible for `cache.get` to return a result more quickly than about 1ms.

For comparison, the in-app has latency lower than 1us (1 microsecond). Using the in-app cache, `[ i.get_currency() for i in Security.objects.all()[0:50] ]` runs in 5-7ms.

Of course, if your memcached server is on the same box as the webserver, latency won't be a problem.

(Side note: I believe the reason the database was nearly as fast as memcached is because the `Currency` table was already sitting in the operating system's disk cache, minimizing disk seeks. This is possible due again to how few currencies actually exist.)

## Use Django's Managers to do it automatically

There are two problems with the approach described above. The first is that it's ugly, the second is that programmers will forget to do it. The result will be inconsistent code style, and some views will wind up slower than they need to be simply because the guy writing them used `security.currency` rather than `security.get_currency()`.

Fortunately, Django gives us a way around this: using a custom [Manager](https://docs.djangoproject.com/en/dev/topics/db/managers/). A `Manager` is the object which directly handles making SQL queries - or not, as we will demonstrate here.

When you make a query, say `Security.objects.get(id=6)`, the manager `Security.objects` is used. But we can easily replace it. I wrote a library called [Guacamole](https://github.com/stucchio/Guacamole) which handles this for us. The gist of it is as follows. You first need to override `Currency.objects`:

    from guacamole import InMemoryCachingManager

    class Currency(models.Model):
        name = models.CharField(max_length=256)

        objects = InMemoryCachingManager()


Inside Guacamole, the `InMemoryCachingManager` is an overloaded version of `django.db.models.Manager`. It has this general structure:

    class InMemoryCachingManager(models.Manager):
        use_for_related_fields = True

        def __init__(...)
            ...

        def get_query_set(self):
            return CustomizedQuerySet(self.model)

The `use_for_related_fields` key tells Django to use this manager even for foreign key lookups, e.g. `security.currency`. The `CustomizedQuerySet` class is a subclass of `django.db.models.query.QuerySet`, and is where the real magic happens. `QuerySet` objects have all the lookup methods we know and love - `get`, `filter`, `all`, etc, and we merely need to override `get`.

I gloss over some technical details (which you can find in the [source code](https://github.com/stucchio/Guacamole/blob/master/guacamole/__init__.py), but basically the customized QuerySet class overrides `get` to handle the caching.

Once this is done, if a `Currency` is already in the cache, then `security.currency` runs in microseconds and does not touch the database.

At this point, we don't need to worry about whether the other guy writing views remembers to use `security.get_currency()` - accessing `security.currency` will still be fast.

## Speeds up your entire site

Another advantage of using Django's managers is that this effort will speed up your entire site. For free. By using in-app caching, you can make small to medium performance improvements on virtually every page that uses `Currency` objects - on a financial site that is likely to be quite a few pages.

As an example, at [Styloot](http://styloot.com), we used this technique inside our product app. This is the app which handles fashion items, brands, vendors, etc - pretty much the only page on the site that doesn't use this app is the "About" page. The net result was that we shaved 400ms off our search queries, we made our wishlist noticeably faster, our embeddable widgets were about 15ms faster, and the load on our database dropped considerably.

In-app caching has the potential to speed up a lot of your pages by a little bit, and a few pages by significant margins. Your webserver likely has at least 1.7GB of RAM (a small ec2 instance), more likely 4-16GB. Using a little of that memory to reduce your network and database usage is a very easy win.
