title: Assorted links
date: 2015-08-27 9:31:00
author: Chris Stucchio
nolinkback: true

# Computing and Mathematics

I've gotten into [Count Min Sketch](https://7797b024-a-62cb3a1a-s-sites.googlegroups.com/site/countminsketch/cm-latin.pdf) lately. It's a neat probabilistic algorithm for counting, and it has the nice property that you can compute inner products with it. More [papers](http://www.aclweb.org/anthology/D12-1100) on the [topic](http://dimacs.rutgers.edu/~graham/pubs/papers/cmencyc.pdf).

[How can I use nonconstructive proofs in data analysis?](http://dataorigami.net/blogs/napkin-folding/55662211-how-can-i-use-non-constructive-proofs-in-data-analysis)

[Distribution Testing: Do It With Class!](https://mittheory.wordpress.com/2015/08/09/distribution-testing-do-it-with-class/) This article discusses how to test whether a piece of code `c` properly implements a probability distribution. Specifically, it discusses the problem of distinguishing (with high probability) between the cases `c in P` (for `P` a class of probability distributions) or alternatively `total_variation_distance(c,P) > epsilon`. Great article.

[The long term effects of A/B testing](https://ewulczyn.github.io/What%20if%20AB%20Testing%20is%20like%20Science/)

[Searching 20 GB/sec: Systems Engineering Before Algorithms](http://blog.scalyr.com/2014/05/searching-20-gbsec-systems-engineering-before-algorithms/) - an oldie but a goodie about brute force log search.

Differential privacy is a really cool topic, relating to running queries on a database while leaking as little information about individuals as possible. But even more interestingly, [machine learning algorithms respecting differential privacy](http://rsrg.cms.caltech.edu/netecon/privacy2015/slides/hardt.pdf) generalize well. In fact, such algorithms can adaptively reuse a holdout set while training themselves, which is pretty awesome (see also the [formal paper](http://arxiv.org/pdf/1504.05800v1.pdf)). More [slides](http://www.mrtz.org/papers/focs10.pdf) on differential privacy, a [practical paper](http://jcse.kiise.org/files/V7N3-04.pdf) on the topic, a [broad overview](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf) and a nice survey from a [statistical point of view](http://www.cse.psu.edu/~ads22/pubs/2008/DworkSmith.pdf). Another article on [adaptive data analysis](http://arxiv.org/pdf/1411.2664v2.pdf), also interesting.

The National Heart, Lung and Blood institute compared the number of positive results in studies which pre-registered their methodology, and studies which didn't. [You'll never believe what happened next.](http://www.plosone.org/article/fetchObject.action?uri=info:doi/10.1371/journal.pone.0132382&representation=PDF) (Hint: preregistration drastically decreased the number of statistically significant results.) One interesting and slightly surprising result is that industry funding was not associated to statistically significant results.

[A small sample study](http://download.springer.com/static/pdf/224/art%253A10.1007%252Fs13164-015-0282-z.pdf?originUrl=http%3A%2F%2Flink.springer.com%2Farticle%2F10.1007%2Fs13164-015-0282-z&token2=exp=1439807370~acl=%2Fstatic%2Fpdf%2F224%2Fart%25253A10.1007%25252Fs13164-015-0282-z.pdf%3ForiginUrl%3Dhttp%253A%252F%252Flink.springer.com%252Farticle%252F10.1007%252Fs13164-015-0282-z*~hmac=175efe82960c5580825edd4cf0263a360e9206097fe0cc3e09aef514449ced3d) finds correlations between results which people find morally offensive and results which are not considered to be credible. Monetary rewards for "correct" answers slightly improves the story (yay for markets!).

[Are ClinicalTrials.gov p-values clustered around 0.05?](http://www.statwonk.com/blog/are-clinicaltrialsgov-p-values-clustered-around-005/)

# Economics and Social Sciences

[The Market for Silver Bullets ](http://iang.org/papers/market_for_silver_bullets.html) - about selling computer security. Apparently security markets are highly inefficient - neither lemon nor lime markets, since both buyer and seller can be clueless.

[Evolution is Not Relevant to Sex Differences in Humans Because I Want it That Way! Evidence for the Politicization of Human Evolutionary Psychology](http://www.evostudies.org/pdf/GeherVol2Iss1.pdf). It's a small sample size, so take with an appropriate grain of salt, but it presents evidence that much of the distaste for evolutionary psychology is solely about disliking the implications for sex differences in humans.

[Mumbai is The World's Most Paradoxical Real Estate Market](https://www.proptiger.com/guide/post/the-worlds-most-paradoxical-real-estate-market-is-in-india-infographic). I've said before that I really want economists to focus more attention on India - things like this are why.

[Great article on how to make commuter rail efficient.](https://pedestrianobservations.wordpress.com/2015/07/26/why-labor-efficiency-is-important/) Hint: eliminate conductors.

[The End of Asymmetric Information](http://www.cato-unbound.org/2015/04/06/alex-tabarrok-tyler-cowen/end-asymmetric-information)

[Gwern's Iron Law of Social Programs](http://www.gwern.net/docs/1987-rossi). Iron law: "The expected value of any net impact assessment of any large scale social program is zero." Stainless Steel Law: "The better designed the impact assessment of a social program, the more likely is the resulting estimate of net impact to be zero."

# Politics and Culture

[The Rule of Law in the Regulatory State](http://johnhttp://dimacs.rutgers.edu/~graham/pubs/papers/cmencyc.pdfhcochrane.blogspot.in/2015/08/rule-of-law-in-regulatory-state.html). This is a fantastic article by John Cochrane discussing how the modern regulatory state has more or less eliminated the rule of law. The general idea is that many projects require pre-approval from regulatory agencies; these agencies use vaguely defined rules and arbitrary delays in order to hinder political opponents. This article provides a lot of detail to support various claims that neoreactionary types make.

[Antiracism - our flawed new religion](http://www.thedailybeast.com/articles/2015/07/27/antiracism-our-flawed-new-religion.html).

[http://www.ribbonfarm.com/2015/08/06/frontierland/](Frontierland). This article discusses theme parks, and the most interesting part (and the reason I'm citing it) is about how frontier culture can be damaging in the long run. The essential argument is that people move from their old lands to the frontier, give up most of their old culture (which has evolved to work well in civilized lands) and replace it with frontier culture (useful primarily for surviving in frontier territory).

[Anti-technology terrorists ally with Marathi Nationalists and launch terror campaign against uber drivers](http://newsroom.uber.com/mumbai/2015/08/keepmaharashtramoving/).

# Biology

[“Ethnic Genetic Interests” Do Not Exist (Neither Does Group Selection)](https://jaymans.wordpress.com/2015/08/02/ethnic-genetic-interests-do-not-exist-neither-does-group-selection/). It's unfortunate that he needs to debunk this, and that such nonsense is becoming so widespread in certain contrarian spheres.

[The Fable of the Dragon Tyrant](http://www.nickbostrom.com/fable/dragon.html) - an interesting article about aging research.

[Is Prostate Cancer Screening Worthless?](http://econlog.econlib.org/archives/2015/08/is_prostate_scr.html) Answer yes. But the answer is delivered very nicely with an "icon box" visualization.
