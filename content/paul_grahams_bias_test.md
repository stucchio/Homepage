title: The Mathematics of Paul Graham's Bias Test
date: 2015-11-03 09:00
author: Chris Stucchio
tags: bias detection, frequentist statistics, statistics
mathjax: true


A major problem in detecting biased decisionmaking is the problem of unknown inputs. For example, suppose a venture capitalist has a public portfolio which has funded 75% male founders and 25% female. Is this venture capitalist biased against women? It's impossible to know - perhaps only 10% of his applicants were female, in which case he might actually biased in favor of women.

Paul Graham recently wrote an article, [A Way to Detect Bias](http://www.paulgraham.com/bias.html), postulating a statistical test which might be usable for detecting bias in a decision process *without looking at the inputs*:

>Think about what it means to be biased. What it means for a selection process to be biased against applicants of type x is that it's harder for them to make it through. Which means applicants of type x have to be better to get selected than applicants not of type x. [1] Which means applicants of type x who do make it through the selection process will outperform other successful applicants.

Paul Graham then proposes a test for checking the bias between two groups, A and B - measure the *mean* performance of members of a and be who have passed the selection process. If these means differ significantly, then the decision process is biased against the group with the higher mean.

As an example of how this might work, let A and B both be exponentially distributed with decay rate $@ \lambda $@. Suppose our selection process imposes a cutoff of $@ C $@, but is biased against group B to the extent of $@ K $@. I.e., a member of A must be at least as good as $@ C $@, whereas a member of B must be at least as good as $@ C + K $@ to be selected.

The distribution of people who have been selected then looks like this:

![bias on selected distributions](/blog_media/2015/paul_grahams_bias_test/effect_of_bias.png)

As a result, the mean of the B selected group is higher by the amount $@ K $@ and therefore the decision process is biased against this group by $@ K $@.

Unfortunately, using the *mean* as a test statistic is flawed - it only works when the pre-selection distribution of A and B is identical, at least beyond C. WildUtah on Hacker News came up with a [counterexample](https://news.ycombinator.com/item?id=10484062):

> Consider two groups of candidates for a scholarship, A and B. We want to select all candidates that have an 80% or better chance of graduation. Group A comes from a population where the chance of graduation is distributed uniformly from 0% to 100% and group B is from one where the chance is distributed uniformly from 10% to 90%, with the same average but less variation in group B.
>
> Now suppose that we select without bias or inaccuracy all the applicants that have an 80% or better chance of graduation. That means we select a subset of A with a range of 80% to 100% and a subset of B with a range from 80% to 90%. The average graduation rate of scholarship winners from group A will be 90% and that from group B will be 85%.

However, there is a way to fix this - take the *minima* of group A members who were selected, and compare the difference of these minima. Concretely, let $@ \vec{a} \subseteq A $@ be the A-members who were selected, and $@ \vec{b} \subseteq B $@ be the B-members selected. Then the test statistic is:

$$ t = \min \vec{a} - \min \vec{b} $$

In both the examples above, this test statistic works. In my graph, $@ t = -K $@ while in WildUtah's example, $@ t = 0 $@.

In fact, I can prove mathematically that this method is a valid non-parametric test. It will work for any distribution of A and B, provided both sets A and B have a finite probability of having members larger than $@ x=C $@.

## What are the ingredients for a frequentist hypothesis test?

For a frequentist hypothesis test, there are two requirements.

*First*, we need to have a null hypothesis. In our case, the null hypothesis will be that the selection process is unbiased, and that the minima of both the A and B distributions are identical. We'll assume further that there is a finite and bounded probability of finding elements of A and B near the cutoff. We don't assume we know what the cutoff is.

Once we have the null hypothesis, we need to prove that *if the null hypothesis is true*, the probability of observing a false positive is bounded. I.e., we need to prove that:

$$p = P( |t| > \epsilon| \textrm{null} ) \leq \delta $$

with the property that as $@ \epsilon $@ increases, $@ \delta $@ decreases. This is a bound on the *false positive* probability of the test, or the probability of type 1 error.

*Second*, we need an alternative hypothesis. In our case, this will be that the distribution $@ b(x) $@ is supported on an interval [C+k, \infty) $@. Once we have this, we need to prove that:

$$ P( |t| < \epsilon| \textrm{alt} ) \leq \delta $$

for some (probably different) $@ \epsilon, \delta $@. This means that *if the alternative hypothesis is true*, the probability of observing a false negative is bounded.

## The test

So here it is.

**Theorem 1:** Take as a null hypothesis the belief that A-members who were selected have the cumulative distribution function $@ a(x) $@ and B-members who were selected have the cdf $@ b(x) $@. Further, we assume that there exists a monotonically increasing function $@ 0 \leq h(x) $@ such that $@ a(x) > h(x) $@ and $@ b(x) > h(x) $@. Then assuming this null hypothesis is true, the probability of observing a result at least as extreme as $@ t $@ is bounded above by:

$$ p \leq \hat{p} = (1-h(C+t/2))^{N_a} + (1-h(C+t/2))^{N_b} $$

This theorem is proved in Appendix 1 at the end of this post.

In simple terms, this means that for any probability distributions $@a(x)$@ and $@ b(x) $@ which have enough mass near $@ x=C $@, the probability of false positives using this statistical test is bounded.

We have a similar theorem for statistical power:

**Theorem 2:** Take as an alternative hypothesis that $@ a(x) $@ is supported in $@ [C,\infty] $@ and is bounded below by $@ h(x) $@ as above. However, suppose that $@ b(x) $@ is supported on $@ [C+K,\infty) $@. Then the probability of a false negative is bounded by:

$$ (1-h(C+K))^{N_a} $$

The proof of this is very simple, so I'll do it right here:

**Proof:** The only way that $@ t $@ can be smaller than $@ K $@ is if every member of $@ \vec{a} $@ is at least as large as $@ C+K $@. The probability of this occurring is $@(1-a(C+K))^{N_a} \leq (1-h(C+K))^{N_a} $@. **QED.**

# Appendix 1: Proof of Theorem 1

The probability of drawing $@ N_a $@ samples from $@ a(x) $@ and none being contained in $@ [C,C+d/2] $@ is $@ (1-a(C+d/2))^{N_a} \leq (1-h(C+d/2))^{N_a}$@, and similarly for $@ b(x) $@ and $@ N_b $@.

Thus, the probability of drawing $@ N_a$@ and $@ N_b $@ samples, at least one of which is contained *within* $@ [C,C+d/2] $@ is bounded below by:

$$
q = 1 - (1-h(C+d/2))^{N_a} - (1-h(C+d/2))^{N_b}
$$

Thus, with probability at least $@ q $@, $@ \min \vec{a} \in [C,C+d/2] $@ and $@ \min \vec{b} \in [C,C+d/2] $@. When this occurs, the test statistic is bounded (in absolute value) by $@d/2 + d/2 = d $@.

Inverting this, we find that with probability *at most* $@ \hat{p} = 1-q $@, the test statistic $@ t = \min \vec{a} - \min \vec{b} $@ will be larger than $@ d $@. Thus:

$$ \hat{p} = (1-h(C+t/2))^{N_a} + (1-h(C+t/2))^{N_b} $$

is an upper bound on the p-value of the hypothesis test.
