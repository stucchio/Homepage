title: Assorted links
date: 2015-01-06 9:30:00
author: Chris Stucchio
nolinkback: true

![archiwindow](http://payload246.cargocollective.com/1/13/424998/7220369/01_the-shining-01_905.jpg)

[Archiset](http://federicobabina.com/ARCHISET) - a wonderful set of architectural and movie illustrations. Actually look at nearly everything by [Federico Babina](http://federicobabina.com/).

[Bayesianism and Causality, or Why I am only a Half-Bayesian](http://ftp.cs.ucla.edu/pub/stat_ser/r284-reprint.pdf). Great article introducing issues of causality in scientific inference.

[Ultrametric semantics of reactive programs](http://research.microsoft.com/pubs/135433/frp-lics11.pdf). This paper describes how to encode causality (the property that a stream function depends only on past values) in the type system. The specific mechanism is an [ultra-metric space](https://en.wikipedia.org/wiki/Ultrametric_space) - specifically, a distance function defined roughly as `d(stream1, stream2) = pow(0.5,n)` where `n` is the first time at which the streams differ.

Finally getting around to reading [Universal Portfolios](http://www-isl.stanford.edu/~cover/papers/paper93.pdf) by Thomas Cover. This describes a portfolio allocation strategy roughly analogous to adversarial bandit algorithms - a prediction-free strategy which should (in the long run) achieve better returns than any constant portfolio.
