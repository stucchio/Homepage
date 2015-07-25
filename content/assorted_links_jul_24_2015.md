title: Assorted links
date: 2015-07-24 9:31:00
author: Chris Stucchio
nolinkback: true

[The Algebra and Calculus of Algebraic Data Types](https://codewords.recurse.com/issues/three/algebra-and-calculus-of-algebraic-data-types/).

[Too Much Finance or Statistical Illusion?](http://www.piie.com/publications/pb/pb15-9.pdf). Very important econometric note: quadratic regression with any variable that rises with per capita income (e.g., doctors, finance, telephones) will cause a negative quadratic term - i.e., past a certain point, that quantity will be predicted to reduce growth.

[Decision Making Under Uncertainty: An Introduction to Robust Optimization](http://blog.yhathq.com/posts/decision-making-under-uncertainty.html) and [part 2](http://blog.yhathq.com/posts/decision-marking-under-uncertainty-2.html). Nice introductory article.

[Functional Error Accumulation in Scala](http://longcao.org/2015/07/09/functional-error-accumulation-in-scala)

[A Dynamic Programming Solution to A/B Test Design](http://www.win-vector.com/blog/2015/07/dynamic-prog-ab-test-design/). A nice article on bandit algorithms (not A/B testing strictly speaking) that almost, but doesn't quite, derive the [Gittins Index](https://en.wikipedia.org/wiki/Gittins_index).

[Adaptive Range Filters for Cold Data: Avoiding Trips to Siberia](http://www.vldb.org/pvldb/vol6/p1714-kossmann.pdf). The article describes a nice data structure, the Adaptive Refinement Tree, which handles *range* queries - it answers the question "does a set S (with ordered elements) contain any elements in the range [l,r]"? It purports to be the range equivalent of Bloom Filters, but this is a bit misleading - the ARF requires an oracle to determine whether the answer it provided is a false positive or not. (For the database applications presented, an oracle is always available, however.)

[An Alternative to Null-Hypothesis Significance Tests](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1473027/pdf/nihms5428.pdf). This paper pushes *replicability* - the probability that future experiments will return results with the same sign as the existing result. An interesting way to think about it, though in my view too focused on experimental methods and not focused enough on actually explaining the world.

[From monoids to near-semirings: the essence of MonadPlus and Alternative](http://people.cs.kuleuven.be/~tom.schrijvers/Research/papers/ppdp2015.pdf). This paper derives a very nice conclusion - just as Monads are Monoids in the category of Endofunctors, Non-Determinism Monads are Near-Semirings in the category of Endofunctors. Pretty definitively, some category theory is required to understand this.

[Introduction to Incremental](https://blogs.janestreet.com/introducing-incremental/) - Jane St. Capital's new library for incremental computation. The basic idea is to define the computation as a DAG, and then the library will incrementally update the DAG components which have changed.

[Investigating and Improving Undergraduate Proof Comprehension](http://www.ams.org/notices/201507/rnoti-p742.pdf). Great line: "This was a humbling reminder that good pedagogical intentions do not always translate into effective interventions."

[What is the expectation maximization](http://ai.stanford.edu/~chuongdo/papers/em_tutorial.pdf)

[Power Laws in Venture Capital](http://reactionwheel.net/2015/06/power-laws-in-venture.html)

[Anti-technology Terrorists Attack Competing Workers](http://techcrunch.com/2015/06/25/french-anti-uber-protest-turns-to-guerrilla-warfare-as-cabbies-burn-cars-attack-uber-drivers/). According to Courtney Love, the police [seem complicit](https://twitter.com/Courtney/status/614033151984205824).

[Frequency Counting Algorithms over Data Streams](http://micvog.com/2015/07/18/frequency-counting-algorithms-over-data-streams/). Nice introductory article.

[The Copenhagen Interpretation of Ethics](http://blog.jaibot.com/the-copenhagen-interpretation-of-ethics/). The Copenhagen Interpretation of Ethics says that you when you observe or interact with a problem in any way, you can be blamed for it. At the very least, you are to blame for not doing more. This philosophy is very relevant to a variety of topics - e.g., minimum wages, trading with poor countries, etc. [Jaibot's blog](http://blog.jaibot.com/) is pretty interesting and has been added to my rss.

[A Cynic’s Guide To Fintech](https://medium.com/bull-market/a-cynic-s-guide-to-fintech-3cd0995e0da3).

[Alex Kozinsky has written a scathing indictment of the American criminal justice system](http://georgetownlawjournal.org/files/2015/06/Kozinski_Preface.pdf). tl;dr; there are lots of people who are wrongfully convicted.

[Ideological Hijacking and Ideological Security](http://thefutureprimaeval.net/socjus-and-ideological-security/). The author discusses the phenomenon of entryism -- outside activists taking over a community (e.g. feminists taking over the reddit anarchist community) -- and how to prevent it.

[Behavioral Public Choice: The Behavioral Paradox of Government Policy](http://www.harvard-jlpp.com/wp-content/uploads/2010/01/ViscusiGayer_4.pdf). Great article applying behavioral economics to public policy.
