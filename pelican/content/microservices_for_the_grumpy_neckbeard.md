title: Microservices for the Grumpy Neckbeard
date: 2014-08-26 08:30
author: Chris Stucchio
tags: scala, java, microservices, service oriented architecture, service objects
mathjax: true
category: scala

Recently microservices have been getting a lot of attention, both positive and negative. Articles about them tend to fall into two camps, which I'll affectionately label the hipster camp and the neckbeard camp. The hipster camp tends to strongly favor microservices, due to the excellent benefits they provide regarding [separation of concerns](http://martinfowler.com/articles/microservices.html), [rigid interfaces](http://www.brunton-spall.co.uk/post/2014/05/21/what-is-a-microservice-and-why-does-it-matter/), localization of data and the like. The neckbeard camp tends to be more suspicious, citing [network latency](http://martinfowler.com/articles/distributed-objects-microservices.html), [network unreliability](http://highscalability.com/blog/2014/4/8/microservices-not-a-free-lunch.html), and the general fact that distributed systems are hard.

In short, the hipsters love the fact that microservices force their code to be clean and isolated, while the neckbeards fear the growth of a massive and unnecessary distributed system.

Fortunately, software archeologists have found an architecture that addresses the concerns of both these camps. In the distant past, Enterprise Java Programmers (TM) faced these problems when building massive internal crud apps at banks and other such dinosaurs. In that distant era, spinning up a new server cluster to solve a problem was not an option - new servers would require forms to be filled out, an operations department to be notified, and permission from one's boss. So these pioneers of computing came up with a solution - a [service object](http://books.google.co.uk/books?id=7dlaMs0SECsC&lpg=PP1&pg=PA106#v=onepage&q&f=false).

# WTF is a microservice?

It's unclear what the "true definition" of a microservice is. I haven't seen a clear definition I can apply to determine that one service is a microservice, while another is a macroservice. So for the purposes of this article, I'll simply use the term "microservice" to denote a service comprising no more than 5,000 lines of code, and exposed via a json-over-http protocol which has at most 5 endpoints.

The key point of a microservice is that over the lifetime of the service, the json-over-http protocol which it exposes is *fixed*. It does not change, which gives the developers implementing it a broad degree of freedom in defining how it works. Consider a service, which we might call `email.internal.enterprise.com`. It exposes a single endpoint which allows the sending of email:

```bash
$ curl -d "{ 'to' : 'foo@bar.com', 'from' : 'test@test.com', ... }"  "http://email.internal.enterprise.com/send"
```

(This example is NOT restful.)

The developers working on Team Email are now solely responsible for making sure this http server properly responds to json-over-http requests. They can address this task in relative isolation, and as long as the task is handled, their job is done.

Alternatively, one might simply expose an SMTP server, but that isn't considered cool anymore.

Consumers of the microservice then access the HTTP endpoint as they see fit:

```python
requests.post("http://email.internal.enterprise.com/send",
              data="{ 'to' : 'foo@bar.com', 'from' : 'test@test.com', ... }",
              ...)
```

Of course, this python code must handle potential problems such as "what if the network is partitioned and I can't reach `email.internal.enterprise.com`". Whether it actually does this in practice is a different question, but in principle this must be handled.

# Service Objects - the Enterprise Programmer(TM) approach

Enterprise Java Programmers have a concept of a *Service Object*. The *Service Object* is an abstraction for the ability to provide some functionality. Lets take email as a working example. We could potentially represent the ability to send email via the following Scala trait:

```scala
trait EmailProvider {
  def sendEmail(to: EmailAddress, from: EmailAddress, subject: String, body: String): Future[EmailSendStatus]
}
```

For those more familiar with Java, this is equivalent to:

```java
interface EmailProvider {
    Future<EmailSendStatus> sendEmail(EmailAddress to, EmailAddress from, String subject, String body)
}
```

The fact that a `Future[EmailSendStatus]` is returned indicates that at the time of calling the method, the result of sending may not be available. I.e., sending the email may take 250ms, but code which does not explicitly depend on the result of `sendEmail` can continue processing while waiting.

In Python, it would probably be:

```python
"""Coding convention. Any object with a `send_email` class member is an `EmailProvider`.
The `email_provider` variable on all the classes in this file should be defined, take
the arguments to, from, subject and body, and do the right thing.
"""
```

This trait/interface (from here on out I'll use Scala terminology) represents the capacity to send emails.

The key fact about this trait/interface is that programmers working on a team other than Team Email are *forbidden* from ever using any interface besides `EmailProvider`. This can generally be enforced at the level of the type system.

## Rigid interface? Check.

Now that we have this service object defined, we get *most* of the benefits of a bonafide microservice. As far as our code is concerned, we get the *same* level of isolation as with the genuine microservice. Team Email exposes no detail about their internal implementations to the world - all they provide is a fixed interface.

When a user wishes to send email, all they get is an object that satisfies this interface. They get no additional information about it. This is typically done with the `Factory` pattern:

```scala
object EmailProviderFactory {
  def getEmailProvider: EmailProvider = ...
}
```

Users may call this method, receive an email provider object, and may only call the known methods on `EmailProvider`. Everything else is opaque to them.

Concretely, what this means is the following. Team Email gets to sit in their office, write nearly any code they like (so long as it doesn't do silly things like `System.exit(-1)`), and simply exposes a rigid interface. Similarly, Team Welcome New Users gets to sit in their office and send emails with the `sendEmail` method. Periodically Team Email will publish an updated jar file which is then consumed by Team Welcome New Users, and email will continue to be sent. Team Welcome New Users has no right to muck around in Team Email's code, and Team Email is free to do as they like within their fiefdom.

## Isolation? Almost.

In terms of isolation, Team Email has *almost* as much isolation as they would in the case of microservices. As a general rule, `EmailProvider` should probably run it's own thread pool, and the number of cores allocated for that thread pool can be constrained. Similarly, `EmailProvider` is in charge of it's own network connections (database, redis, etc), and therefore cannot break resources used by other parties.

In principle it is possible for `EmailProvider` to do bad things - consume ridiculous amounts of memory, drastically increase GC load, or thrash the disk. But in practice these sorts of things are unlikely and nearly always caught in testing.

# The network is unreliable - and so are microservices

Consider the following set of dependencies. `WelcomeNewUsers` must call `sendEmail`. In order to send an email, `sendEmail` must make certain the recipient has not unsubscribed - this requires a call to the user authorization service.

With a microservice based architecture, we have the following network calls:

1. `WelcomeNewUsers` calls the http server at `sendEmail`.
2. The server at `sendEmail` calls the http server at `UserAuthorization`.
3. The server at `UserAuthorization` calls it's primary database, returning the result to the `UserAuthorization` http server.
4. After the `sendEmail` server receives the response, it then connects to the SMTP server and sends the email.

Suppose we now use Service Objects. Steps 1 and 2 are both method calls. Only steps 3 and 4 actually touch the network.

Assuming there is a probability $@\gamma$@ of any one network connection failing, then the probability of failure with a microservices approach is:

$$ 1 - (1 - \gamma)^4 = 4 \gamma - 6 \gamma^2 + 4 \gamma^3 - \gamma^4 \sim 4 \gamma$$

(The $@\sim$@ notation means that provided $@\gamma$@ is small, i.e. the network is almost reliable, then the higher order terms become negligible.)

In contrast, with the Service Object approach, the probability of failure is:

$$ 1 - (1 - \gamma)^2 = 2 \gamma - \gamma^2 \sim 2 \gamma $$

So the error rate of the microservice approach caused by network problems will be twice that of the service object approach. Additionally, the network latency incurred by the Microservice approach is almost double that of the Service Object approach, since the microservices approach requires 4 round trips rather than 2.

# Switching to microservices is easy

Suppose we took a Service Object approach to application infrastructure and it turns out to be wrong. It turns out that `EmailProvider` actually thrashes the network, makes way too many disk seeks and overloads the garbage collector. It needs to run in it's own separate process.

What now?

The answer is pretty simple - Team Email needs to switch to a microservice. Here is how that happens:

1. Team Email builds the microservice.
2. Team Email builds a new version of `EmailProvider` which calls the microservice and then publishes a new jar.

Because of the Service Object approach, everyone else's code is already structured to handle microservices. This makes actually replacing the service object with a

# Service Objects make testing fun

An additional benefit of service objects is that they make testing easy. To test the success case:

```scala
class FakeSuccessfulEmailProvider extends EmailProvider {
  def sendEmail(to: EmailAddress, from: EmailAddress, subject: String, body: String): Future[EmailSendStatus] = Future { EmailSuccess(EmailAddress("testguy@test.com")) }
}

val userWelcomeSent = sendWelcomeEmail(fakeUser, new FakeSuccessfulEmailProvider)
assert( Await.result(userWelcomeSent) === EmailSuccess(EmailAddress("testguy@test.com")) )
```

Similar examples can be provided for common errors, e.g. timeout:

```scala
class FakeTimeoutEmailProvider extends EmailProvider {
  def sendEmail(to: EmailAddress, from: EmailAddress, subject: String, body: String): Future[EmailSendStatus] = Future {
    Thread.sleep(60000)
    EmailSuccess(EmailAddress("testguy@test.com"))
  }
}

val userWelcomeSent = sendWelcomeEmail(fakeUser, new FakeTimeoutEmailProvider)
assert( Await.result(userWelcomeSent) === EmailFailure(Timeout) )
```

# Fear the Network more than the Monolith

When building reliable software, the network is your enemy. Distributed systems are simply hard. Sometimes you need to build them, but why do so before it becomes necessary? Service Objects provide most of the encapsulation benefits of microservices without the hassle of really building a distributed system.

As for the rest of us, it's important to note that even Enterprise Java Programmers (TM) have a few useful tricks up their sleeve. This is certainly one of them.
