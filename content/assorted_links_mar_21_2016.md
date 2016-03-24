title: Assorted links
date: 2016-03-25 9:30:00
author: Chris Stucchio
nolinkback: true

## Computer science and math

[Principal Component Projection Without Principal Component Analysis](http://arxiv.org/pdf/1602.06872v1.pdf) - yep, this is as awesome as it sounds.

[String Interning done Right](https://getkerf.wordpress.com/2016/02/22/string-interning-done-right/) - from Scott Locklin. From what I can tell, it's a bit specific to column oriented databases where the main string field contain highly repeated small values like "SPY" or "ARCA", but it's still a great read.

[The Power of Simple Tabulation Hashing](https://people.csail.mit.edu/mip/papers/charhash/charhash.pdf). This paper discusses an alternative to Bloom filters, for the special case when objects being hashed are random strings of fixed length, as opposed to arbitrary hashable objects, and shows that they can behave significantly better than Bloom filters. This is an important use case - for instance, hashing of UUIDs or other fixed length identifiers.

[Why CSP Matters](http://reaktor.com/blog/why-csp-matters-i-keeping-things-in-sync/) - nice article on CSP in Clojure.

[Design for experts; accomodate beginners](https://pchiusano.github.io/2016-02-25/tech-adoption.html). An interesting article advocating that to get adoption, a technology should attempt to accomodate beginners. A better solution would be for culture to become less short term, and unwillingness to learn become less socially acceptable. In light of this article, one can ask the question - is Go evil? It's a language designed to be easy to learn, but which provides no real benefits over competitors (such as Scala, Haskell or Rust).

[Nice Akka Stream tutorial](https://medium.com/@kvnwbbr/diving-into-akka-streams-2770b3aeabb0)

[Comment on 'Estimating the Reproducibility of Psychological Science'](http://datacolada.org/wp-content/uploads/2016/03/5321-Gilbert-et-al-Comment-on-reproducibility.pdf) - critiques the original replicability project. Gelman [continues to be pessimistic](http://andrewgelman.com/2016/03/05/29195/). [Data Colada](http://datacolada.org/2016/03/03/47/) points out flaws in both. [More commentary](https://hardsci.wordpress.com/2016/03/03/evaluating-a-new-critique-of-the-reproducibility-project/). Also note that *everyone is misinterpreting confidence intervals* - exactly as [predicted](http://www.ejwagenmakers.com/inpress/HoekstraEtAlPBR.pdf) in a different psychology paper.

[Maximum Entropy from Bayes Theorem](https://qchu.wordpress.com/2016/03/06/maximum-entropy-from-bayes-theorem/)

[Reckoning with the past](http://michaelinzlicht.com/getting-better/2016/2/29/reckoning-with-the-past) - in which a scientist discusses the possibility that his life's work might be wrong.

[The Harmonic Mean of the Likelihood: Worst Monte Carlo Method Ever](https://radfordneal.wordpress.com/2008/08/17/the-harmonic-mean-of-the-likelihood-worst-monte-carlo-method-ever/)

[A great article](http://www.terryburnham.com/2015/04/a-trick-for-higher-sat-scores.html) about how bad scientific ideas with "meme"-entum survive.

## Trading and Economics

[A Quant's Approach to Building Trading Strategies, pt 2](https://www.quandl.com/blog/interview-with-a-quant-part-two). And [part 3](https://www.quandl.com/blog/interview-with-a-quant-part-three).

[Tweetstorm about "The Rise and Fall of American Growth"](https://storify.com/withinepsilon/gordon-inequality).

[Facts about Billionaires](http://conversableeconomist.blogspot.com/2016/02/facts-about-billionaires.html). In the US, the percentage of billionaires who have inherited wealth is dropping, contradicting Piketty.

[Why Minimum Wages can take Time to Destroy Jobs](http://econlog.econlib.org/archives/2016/02/why_minimum_wag.html). Great article illustrating the effects of fixed costs.

[Closed Borders Advocates Walk Out of Tesla Factory](http://www.bloomberg.com/news/articles/2016-02-29/about-100-workers-walk-out-at-tesla-battery-plant-building-site). Apparently some Nevada workers don't like economic competition from (New) Mexicans.

[Ego depletion is really hard to replicate.](http://www.slate.com/articles/health_and_science/cover_story/2016/03/ego_depletion_an_influential_theory_in_psychology_may_have_just_been_debunked.single.html).

## Culture

[Scott Sumner on why he doesn't use Twitter](http://www.themoneyillusion.com/?p=31553).

Great article on [violence and mental illness](http://siderea.livejournal.com/1256347.html).

A ["tech bro"](https://justink.svbtle.com/open-letter-to-mayor-ed-lee-and-greg-suhr-police-chief) wrote a letter to the Mayor of SF complaining about the homeless. He was widely criticized for it, but the actual letter is worth reading. *"A distraught, and high person was right in front of the restaurant, yelling, screaming, yelling about cocaine, and even, attempted to pull his pants down and show his genitals."* Apparently the "tech bro" believes that a legitimate function of government is preventing such things.

[Uber for Welfare](http://www.politico.com/agenda/story/2016/1/uber-welfare-sharing-gig-economy-000031). A nice article discussing how Welfare to Work can be improved by integrating with the gig economy. Strangely, when I defend this Bill Clinton/FDR-like policy on Hacker News and other such places, folks act as if I'm some extreme right winger.

[Why India Needs it's Quack Doctors](https://www.good.is/articles/why-india-needs-its-quack-doctors).

[Evidence Based Medicine is (micro-)Fascism](https://www.ucl.ac.uk/Pharmacology/dc-bits/holmes-deconstruction-ebhc-06.pdf). What is this I don't even know?

[Math education research is mostly nonsense](https://www.math.upenn.edu/~wilf/website/PSUTalk.pdf). Having read a few papers there, I can't disagree.

[Splain it to me](https://status451.com/2016/01/06/splain-it-to-me/) - great article illustrating how some people perceive communication as sharing knowledge, while others perceive it as raising/lowering status.

[Scott Alexander reviews Trump's book](http://slatestarcodex.com/2016/03/19/book-review-the-art-of-the-deal/).
>Reading about the system makes me both grateful and astonished that any structures have ever been erected in the United States at all, and somewhat worried that if anything ever happens to Donald Trump and a few of his close friends, the country will lose the ability to legally construct artificial shelter and we will all have to go back to living in caves.

Trump is winning because it's socially acceptable to write articles like this: [Working Class Whites Have Moral Responsibilities](http://www.nationalreview.com/corner/432796/working-class-whites-have-moral-responsibilities-defense-kevin-williamson) (which actually discusses mostly the welfare class). But it's not socially acceptable to write a similar article about welfare class blacks, or other privileged groups. Trump is winning because the folks this article discuss believe he's in their corner.

I don't know if I should be more or less shocked about the [Clinton email scandal than before](http://arstechnica.com/information-technology/2016/03/nsa-refused-clinton-a-secure-blackberry-like-obama-so-she-used-her-own/):
> As I had been speculating, the issue here is one of personal comfort… [Secretary Clinton] does not use a computer, so our view of someone wedded to their e-mail (why doesn't she use her desktop when in the SCIF?) doesn't fit this scenario...
> Given the NSA's refusal to give Clinton what she wanted, the secretary apparently decided to continue to use her personal e-mail server for State Department business, while her staff was fully aware of the security risks associated with using her BlackBerry.
