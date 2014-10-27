title: Write Queries with Tiramisu
date: 2012-11-25 11:04
author: Chris Stucchio
tags: algorithms, SQL





By now, it is a fairly uncontroversial opinion that [ORMs](https://en.wikipedia.org/wiki/Object-relational_mapping) create a large number of difficulties when developing larger systems. The have been famously called the [Vietnam of Computer Science](http://blogs.tedneward.com/2006/06/26/The+Vietnam+Of+Computer+Science.aspx). The main alternative to ORMs is manually constructing SQL by hand, but unfortunately that is a rather dangerous thing to do in the present day.



A lot has been written about why you might prefer writing straight SQL to using an ORM, and I feel no need to add to the literature.

## The danger

The fundamental difficulty with manually constructing SQL is that it raises the risk of [SQL Injection](https://en.wikipedia.org/wiki/SQL_injection) attacks. Consider the following method:

    def getItemsBySlug(slug: String): List[Item] = {
        val sqlQuery = "SELECT * FROM items WHERE slug = '" + slug + "';"
	Select(sqlQuery).map(parseItemFromSqlRow)
      }

The danger here is that if the `slug` variable comes from user input, we might run a query different from what we expect:

    getItemBySlug("foo' OR true OR slug = '")

will run the query:

    SELECT * FROM items WHERE slug = 'foo' OR true OR slug = '';

This will return ALL items from the database, rather than simply the items with the desired slug. This is a potential security risk.

This is typically addressed with parameterized queries. For example, using the [Anorm](http://www.playframework.org/modules/scala-0.9/anorm) library, you would do the following:

    def getItemsBySlug(slug: String): List[Item] = {
        val sqlQuery = "SELECT * FROM items WHERE slug = {slug};"
        SQL(sqlQuery).on("slug" -> slug)()
	             .map(parseItemFromSqlRow)
      }

The problem with this approach is that it eventually becomes unwieldy. Very often, you wish to construct SQL from helper functions. For example, suppose you want to allow users to login via either a username/password pair, or via facebook. You'd probably represent user credentials in a manner like this:


    abstract class AuthToken
    case class UsernamePassword(username: String, password: String)
    case class Facebook(token: String)

You may also have several methods using SQL queries, each of which requires an `AuthToken`. If SQL Injection were not a problem, you'd write a method like this:

    def userByAuthTokenClause(ref: AuthToken): String = ref match {
      case UsernamePassword(username, password) =>
           " user.username = '" + username + "' AND user.hashed_password = '" + passwordHash(password) + "' "
      case Facebook(token) => " user.id IN (SELECT user_id FROM facebook_auth WHERE token='" + token + "') "
    }

    ...

    val sqlQuery = "SELECT * FROM users WHERE " + userByAuthTokenClause(authToken)
    SQL(sqlQuery).on()().map(parseUserFromSqlRow)


To be safe, you need to write something more complicated:

    def userByAuthTokenClause(ref: ItemRef): (String, Seq[(String, anorm.ParameterValue[_])]) = ref match {
      case UsernamePassword(username, password) =>
          (" user.username = {username} AND user.hashed_password={hashed_pw} ",
           Seq("username -> username, "hashed_pw" -> passwordHash(password))
          )
      case Facebook(token) => (" user.id IN (SELECT user_id FROM facebook_auth WHERE token={token}) ",
                               Seq("token" -> token)
                              )
    }

    ...

    val (userClause, userParams) = userRefWhereClause(userRef)
    val sqlQuery = "SELECT * FROM users WHERE " + userByAuthTokenClause(authToken)
    SQL(sqlQuery).on(userParams: _*)().map(parseUserFromSqlRow)

Furthermore, if you want to correct a mistake, things might get very complicated. Suppose a developer accidentally wrote the dangerous version of `itemRefWhereClause`, which returns a `String`. Once you correct that method, *every single call site* must be modified since the type signature has changed from `ItemRef => String` to `ItemRef => (String, Seq[(String, anorm.ParameterValue[_])])`.

## Tiramisu - a safe SQL construction library

To make constructing SQL safe, I wrote the library [Tiramisu](https://github.com/stucchio/Tiramisu). Using Tiramisu, you create `Query` objects, which represent both the SQL string together with it's query params. The method `.sql` applied to a `String` turns the `String` into a `Query`:

    import com.chrisstucchio.tiramisu._
    import com.chrisstucchio.tiramisu.Syntax._

    ...

    val query = "SELECT * FROM items WHERE ".sql

At this point, the value `query` represents a SQL query with no parameters. Adding parameters can be done in two ways:

    val query = "SELECT * FROM items WHERE slug={slug};".sqlP("slug" -> slug)
    val query = "SELECT * FROM items WHERE slug=".sql + slug.sqlV + ";"

If the second method is used a random parameter name will be generated, i.e. the resulting sql might be:

    SELECT * FROM items WHERE slug={336cf1ee_7599_49d3_b1a5_626ab58319ee};

Query objects can be composed just like strings. This makes generating and using helper methods easier:

    def userByAuthTokenClause(ref: AuthToken): Query = ref match {
      case UsernamePassword(username, password) =>
           " user.username = {username} AND user.hashed_password={hashed_pw}"
               .sqlP("username" -> username, "hashed_pw" -> passwordHash(password))
      case Facebook(token) => " user.id IN (SELECT user_id FROM facebook_auth WHERE token={token}) "
                                 .sqlP("token" -> token)
    }

    ...

    val sqlQuery = "SELECT * FROM users WHERE " + userByAuthTokenClause(authToken)
    Tiramisu.Select(sqlQuery).map(parseUserFromSqlRow)

Further, it makes fixing errors a lot easier. If some sleepy developer accidentally writes this:

    def fooClause(ident: String): Query = (" foo.ident = '" + ident + ' ").sql

It can be easily fixed as follows:

    def fooClause(ident: String): Query = " foo.ident = ".sql + ident.sqlV

This fix requires no change to either the type signature or resulting code.

You can find [Tiramisu](https://github.com/stucchio/Tiramisu) on [github](https://github.com/stucchio/Tiramisu).
