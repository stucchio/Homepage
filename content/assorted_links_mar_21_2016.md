title: Assorted links
date: 2016-03-20 9:30:00
author: Chris Stucchio
nolinkback: true

## Computer science and math

[Principal Component Projection Without Principal Component Analysis](http://arxiv.org/pdf/1602.06872v1.pdf) - yep, this is as awesome as it sounds.

[String Interning done Right](https://getkerf.wordpress.com/2016/02/22/string-interning-done-right/) - from Scott Locklin. From what I can tell, it's a bit specific to column oriented databases where the main string field contain highly repeated small values like "SPY" or "ARCA", but it's still a great read.

[The Power of Simple Tabulation Hashing](https://people.csail.mit.edu/mip/papers/charhash/charhash.pdf). This paper discusses an alternative to Bloom filters, for the special case when objects being hashed are random strings of fixed length, as opposed to arbitrary hashable objects, and shows that they can behave significantly better than Bloom filters. This is an important use case - for instance, hashing of UUIDs or other fixed length identifiers.

[Why CSP Matters](http://reaktor.com/blog/why-csp-matters-i-keeping-things-in-sync/) - nice article on CSP in Clojure.

[Design for experts; accomodate beginners](https://pchiusano.github.io/2016-02-25/tech-adoption.html). An interesting article advocating that to get adoption, a technology should attempt to accomodate beginners. A better solution would be for culture to become less short term, and unwillingness to learn become less socially acceptable. In light of this article, one can ask the question - is Go evil? It's a language designed to be easy to learn, but which provides no real benefits over competitors (such as Scala, Haskell or Rust).

[Nice Akka Stream tutorial](https://medium.com/@kvnwbbr/diving-into-akka-streams-2770b3aeabb0)

[Replication crisis crisis: Why I continue in my “pessimistic conclusions about reproducibility”](http://andrewgelman.com/2016/03/05/29195/). I agree completely with Gelman.

## Trading and Economics

[A Quant's Approach to Building Trading Strategies, pt 2](https://www.quandl.com/blog/interview-with-a-quant-part-two). And [part 3](https://www.quandl.com/blog/interview-with-a-quant-part-three).

[Tweetstorm about "The Rise and Fall of American Growth"](https://storify.com/withinepsilon/gordon-inequality).

[Facts about Billionaires](http://conversableeconomist.blogspot.com/2016/02/facts-about-billionaires.html). In the US, the percentage of billionaires who have inherited wealth is dropping, contradicting Piketty.

[Why Minimum Wages can take Time to Destroy Jobs](http://econlog.econlib.org/archives/2016/02/why_minimum_wag.html). Great article illustrating the effects of fixed costs.

[Closed Borders Advocates Walk Out of Tesla Factory](http://www.bloomberg.com/news/articles/2016-02-29/about-100-workers-walk-out-at-tesla-battery-plant-building-site). Apparently some Nevada workers don't like economic competition from (New) Mexicans.

## Culture

Great article on [violence and mental illness](http://siderea.livejournal.com/1256347.html).

A ["tech bro"](https://justink.svbtle.com/open-letter-to-mayor-ed-lee-and-greg-suhr-police-chief) wrote a letter to the Mayor of SF complaining about the homeless. He was widely criticized for it, but the actual letter is worth reading. *"A distraught, and high person was right in front of the restaurant, yelling, screaming, yelling about cocaine, and even, attempted to pull his pants down and show his genitals."* Apparently the "tech bro" believes that a legitimate function of government is preventing such things.

[Uber for Welfare](http://www.politico.com/agenda/story/2016/1/uber-welfare-sharing-gig-economy-000031). A nice article discussing how Welfare to Work can be improved by integrating with the gig economy. Strangely, when I defend this Bill Clinton/FDR-like policy on Hacker News and other such places, folks act as if I'm some extreme right winger.

[Why India Needs it's Quack Doctors](https://www.good.is/articles/why-india-needs-its-quack-doctors).

[Evidence Based Medicine is (micro-)Fascism](https://www.ucl.ac.uk/Pharmacology/dc-bits/holmes-deconstruction-ebhc-06.pdf). What is this I don't even know?
