title: The Science of Detecting Bias - how to eliminate troublesome variables
date: 2015-11-08 09:00
author: Chris Stucchio
tags: bias detection, frequentist statistics, statistics
mathjax: true

Last week Paul Graham wrote a bit about the detection of bias - i.e., the question of whether a decision process favors some subgroup in a manner that reduces outputs. Specifically, the decision process receives a set of data points and renders a go/no go decision for each one. The goal is to maximize the output of the selected data points. For example, a venture capitalist receives many pitches and attempts to maximize the returns of the portfolio of pitches that they accept.

Graham proposed a bias test, and then I [waded into the fray](/blog/2015/paul_grahams_bias_test.html) to make his results *technically* correct - the best kind of correct. The cool thing about Graham's test is that one could measure whether a decision process is biased *without looking at the inputs*. Since then I've devoted a bit more thought to the issue, and I've identified a number of other tests of various hypothesis. So rather than discussing *math*, this post is more about identifying good experiments and measurements.

The key idea to coming up with good measurements is

# Hypothesis: Women are discouraged/discriminated against in education

It's well known that considerably fewer women graduate from college with a degree in computer science than men. The question arises as to why this is. One hypothesis is that various factors in the educational system discriminate against women and discourage them from graduating.

If this were true, the net result would be fewer graduating from computing.

On the other hand, suppose women simply had a lower innate ability or interest in computing; this would also result in fewer of them graduating from computing.

Unfortunately, simply looking at the number of women graduating from CS programs does not allow us to distinguish between these theories. Both theories accurately predict reality. In mathematical terms, we have the following relationship:

$$ m_g = m_0 \cdot (1-a_m) \cdot (1-b_m) $$

$$ w_g = w_0 \cdot (1-a_w) \cdot (1-b_w) $$

Here, $@ m_g $@ represents the number of male graduates, $@ m_0 $@ represents the number of men in the population, $@ a_m $@ represents the fraction of men who are discouraged by education, and $@ b_m $@ represents the fraction of men who do not have the innate ability/interest to get into computing. Similarly, $@ a_w $@ is the fraction of women discouraged, etc.

If $@ w_g \ll m_g $@, this can easily be because either $@ a_w > a_m $@ or $@ b_w > b_m $@. At this stage we simply can't know if women are discouraged relative to men without knowing their innate abilities.

## How to test this hypothesis

If we want to tease out the effect of discouragement, we need to find a way to determine what might happen if the $@ (1-a_w) $@ were not present. Fortunately, we have a way to do this - autodidacts!

Autodidacts are people who study computing by themselves, rather than in a formal education system. So if $@ (1-k_w) $@ is the propensity for a woman to become an autodidact, we would have the following relation:

$$ m_g^a = m_0 \cdot (1-k_m) \cdot (1-b_m) $$

$$ w_g^a = w_0 \cdot (1-k_w) \cdot (1-b_w) $$

Here, $@ k_w $@ and $@ k_m $@ are the fraction of men/women who are unable to learn computing as autodidacts. So far I've just rewritten the equation and renamed a variable. But now that we have 4 measurements - the number of male and female graduates, and male/female autodidacts - we can eliminate some variables from the equations:

$$
\frac{m_g^a }{m_g} = \frac{ m_0 \cdot (1-k_m) \cdot (1-b_m) } { m_0 \cdot (1-a_m) \cdot (1-b_m) } = \frac{ (1-k_m) } { (1-a_m) }
$$

$$
\frac{w_g^a }{w_g} = \frac{ w_0 \cdot (1-k_w) \cdot (1-b_w) } { w_0 \cdot (1-a_w) \cdot (1-b_w) } = \frac{ (1-k_w) } { (1-a_w) }
$$

The important thing about these equations is that **we no longer need to know the innate ability/interest of men and women**. They depend on two factors - the ability of men and women to learn independently, and the level of discouragement each group has suffered. Innate ability is eliminated from the theory.

So now suppose concretely that $@ w_g^a / w_g $@ were much larger than $@ m_g^a / m_g $@. This would mean one of two things - either $@ k_w $@ is smaller, or $@ a_w $@ was larger. I.e., either women are better at learning independently than men, or women are more discouraged than men. If we assume men and women have equal learning abilities ($@ k_w = k_m $@), then the only remaining conclusion is that women are more discouraged than men.

Conversely, if these two numbers are equal, then either women are not discouraged more than men, or women are more discouraged but their innate ability to learn independently has exactly compensated for this.

## Determining my belief changes

I don't know where to find data comparing autodidacts to graduates. However, I believe a very valuable scientific exercise is to declare how my beliefs will change in response to new data. So I hereby declare that although I am at present skeptical that women are discouraged, if clean and statistically significant data arrives and shows me that $@ w_g^a / w_g \gg m_g^a / m_g $@, then I will update my beliefs and be convinced that women are discouraged at the ducation stage.
