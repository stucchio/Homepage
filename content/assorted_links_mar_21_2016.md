title: Assorted links
date: 2016-03-20 9:30:00
author: Chris Stucchio
nolinkback: true

## Computer science and math

[Principal Component Projection Without Principal Component Analysis](http://arxiv.org/pdf/1602.06872v1.pdf) - yep, this is as awesome as it sounds.

[String Interning done Right](https://getkerf.wordpress.com/2016/02/22/string-interning-done-right/) - from Scott Locklin. From what I can tell, it's a bit specific to column oriented databases where the main string field contain highly repeated small values like "SPY" or "ARCA", but it's still a great read.

[The Power of Simple Tabulation Hashing](https://people.csail.mit.edu/mip/papers/charhash/charhash.pdf). This paper discusses an alternative to Bloom filters, for the special case when objects being hashed are random strings of fixed length, as opposed to arbitrary hashable objects, and shows that they can behave significantly better than Bloom filters. This is an important use case - for instance, hashing of UUIDs or other fixed length identifiers.

[Why CSP Matters](http://reaktor.com/blog/why-csp-matters-i-keeping-things-in-sync/) - nice article on CSP in Clojure.

## Trading

[A Quant's Approach to Building Trading Strategies, pt 2](https://www.quandl.com/blog/interview-with-a-quant-part-two).

## Culture

A ["tech bro"](https://justink.svbtle.com/open-letter-to-mayor-ed-lee-and-greg-suhr-police-chief) wrote a letter to the Mayor of SF complaining about the homeless. He was widely criticized for it, but the actual letter is worth reading. *"A distraught, and high person was right in front of the restaurant, yelling, screaming, yelling about cocaine, and even, attempted to pull his pants down and show his genitals."* Apparently the "tech bro" believes that a legitimate function of government is preventing such things.

[Uber for Welfare](http://www.politico.com/agenda/story/2016/1/uber-welfare-sharing-gig-economy-000031#ixzz3yfWmNK9i). A nice article discussing how Welfare to Work can be improved by integrating with the gig economy.

[Why India Needs it's Quack Doctors](https://www.good.is/articles/why-india-needs-its-quack-doctors).
