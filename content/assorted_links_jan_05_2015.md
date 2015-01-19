title: Assorted links
date: 2015-01-20 9:30:00
author: Chris Stucchio
nolinkback: true

![archiwindow](http://payload246.cargocollective.com/1/13/424998/7220369/01_the-shining-01_905.jpg)

[Archiset](http://federicobabina.com/ARCHISET) - a wonderful set of architectural and movie illustrations. Actually look at nearly everything by [Federico Babina](http://federicobabina.com/).

[Bayesianism and Causality, or Why I am only a Half-Bayesian](http://ftp.cs.ucla.edu/pub/stat_ser/r284-reprint.pdf). Great article introducing issues of causality in scientific inference. Most important point - "Causal assumptions, in contrast [to statistical assumptions], cannot be verified even in principle, unless one resorts to experimental control." Another great quote: "The third resistance to causal (vis-a-vis statistical) assumptions stems from their intimidating clarity...assumptions about how variables cause one another are shockingly transparent, and tend therefore to invite counter-arguments and counter-hypotheses." After reading this, I'm inclined to learn more about various attempts at a causal calculus, particularly the [Do Calculus](http://arxiv.org/pdf/1305.5506v1.pdf).

[Ultrametric semantics of reactive programs](http://research.microsoft.com/pubs/135433/frp-lics11.pdf). This paper describes how to encode causality (the property that a stream function depends only on past values) in the type system. The specific mechanism is an [ultra-metric space](https://en.wikipedia.org/wiki/Ultrametric_space) - specifically, a distance function defined roughly as `d(stream1, stream2) = pow(2,-n)` where `n` is the first time at which the streams differ.

[Machine Learning: The High-Interest Credit Card of Technical Debt](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43146.pdf). This article gives a broad overview of how many ML systems are (unavoidably) poorly engineered and suffer many of the problems of bad code. E.g., unused or weakly used dependencies, unexpected feedback loops. Very important read for anyone building such systems.

Yet again I found myself re-reading [Universal Portfolios](http://www-isl.stanford.edu/~cover/papers/paper93.pdf) by Thomas Cover. This describes a portfolio allocation strategy roughly analogous to adversarial bandit algorithms - a prediction-free strategy which should (in the long run) achieve better returns than any constant portfolio. The proof is interesting. The strategy is first shown to have returns equal to the integral over all possible constant portfolios. Then the Laplace method of integration guarantees that the average converges to the best.

[The Big Problem is Medium Data](http://highscalability.com/blog/2014/12/17/the-big-problem-is-medium-data.html)

[A key part of statistical thinking is to use additive rather than Boolean models](http://andrewgelman.com/2014/12/18/key-part-statistical-thinking-use-additive-rather-boolean-models/)

[What effect size would you expect](http://blog.dansimons.com/2013/03/what-effect-size-would-you-expect.html). Discusses what specific measurement should count as a "replication".

[Ten lessons learned from building real ML systems](http://technocalifornia.blogspot.in/2014/12/ten-lessons-learned-from-building-real.html).

[Spoofers Tricked High-Speed Traders by Hitting Keys Fast](http://www.bloombergview.com/articles/2015-01-13/spoofers-tricked-highspeed-traders-by-hitting-keys-fast)

[Poor in the US = Rich](http://blog.givewell.org/2009/11/27/poor-in-the-us-rich/). A short article with many links, and given that this is from [givewell.org](http://givewell.org), it suggests why resources should be diverted from helping poor/rich Americans to helping actual poor people elsewhere. Also notable: [Hunger here vs hunger there](http://blog.givewell.org/2009/11/26/hunger-here-vs-hunger-there/).

Apparently [Shanley Kane was a great big racist](http://www.breitbart.com/london/2015/01/17/i-taught-shanley-kane-how-to-troll-and-im-sincerely-sorry/). The horrible weev-kind. Her twitter feed pretty much admits it's true.

[How regulators (ab)use bank regulation for non-democratic purposes](http://dailycaller.com/2015/01/14/audio-tapes-reveal-how-federal-regulators-shut-down-gun-store-owners-bank-accounts/).

If I ever find myself in a situation where I have a gas oven, I'll be sure to [bake a french toast rosat](https://imgur.com/gallery/MPQDR).

![french toast roast](https://i.imgur.com/molopdl.jpg)

[Gawker publishes an article semi-apologizing for spawning a lynch mob](http://gawker.com/justine-sacco-is-good-at-her-job-and-how-i-came-to-pea-1653022326). Well, also defending themselves, now that they are the victim of one.
