title: Easy Evaluation of Decision Rules in Bayesian A/B testing
date: 2014-06-05 09:30
author: Chris Stucchio
tags: ab testing, bayesian statistics, ab testing
mathjax: true





Earlier this year I published a blog post about a [Baysian decision rule](http://www.bayesianwitch.com/blog/2014/bayesian_ab_test.html) for choosing between two variations, each with a potentially different conversion rate. The basic idea of the decision rule is as follows.

1. Choose a "threshold of caring" - if A and B differ by less than this threshold, you don't care which one you choose.
2. Choose a prior on the distribution of conversion rates of A and B.
3. Compute a posterior, and use it to estimate whether the expected losses you'd make by choosing A (or B) are below the threshold of caring. If so, stop the test.

This A/B testing procedure has two main advantages over the standard Students T-Test. The first is that unlike the Student T-Test, you can stop the test early if there is a clear winner or run it for longer if you need more samples. The second is that as a Bayesian test, your outputs are easily interpreted quantities - for example, the probability that version A is better than version B, or your expected loss from choosing the wrong one.



I won't repeat the [details of the method](http://www.bayesianwitch.com/blog/2014/bayesian_ab_test.html), instead referring the reader to the original post. The crucial part of the test is determining when to stop. Suppose version A has a higher empirical mean than version B, i.e. $@ \textrm{clicks on A} / \textrm{displays of A} > \textrm{clicks on B} / \textrm{displays of B} $@. Then the test is stopped when:

$$ \int_0^1 \int_0^1 \max(x-y,0) \frac{x^a(1-x)^b}{B(a,b)} \frac{y^c(1-y)^d}{B(c,d)} dx dy \leq \textrm{threshold of caring}$$

Or, to simplify:

$$ \int_0^1 \int_y^1 (x-y) \frac{x^a(1-x)^b}{B(a,b)} \frac{y^c(1-y)^d}{B(c,d)} dx dy \leq \textrm{threshold of caring}$$

In the [original blog post](http://www.bayesianwitch.com/blog/2014/bayesian_ab_test.html), the integral is calculated numerically. However, it turns out we can compute it exactly using the following formula. Define first the function:

$$ h(a,b,c,d) = 1 - \sum_{j=0}^{c-1} \frac{B(a+j,b+d) }{(d+j)B(1+j,d)B(a,b) } $$

Note that $@ h(a,b,c,d) = P(X > Y) $@ where $@ X \sim \beta(a,b) $@ and $@ Y \sim \beta(c,d) $@.

Then:

$$ \int_0^1 \int_y^1 (y-x) \frac{x^a(1-x)^b}{B(a,b)} \frac{y^c(1-y)^d}{B(c,d)} dx dy = \frac{B(a+1,b)}{B(a,b)} h(a+1,b,c,d) - \frac{B(c+1,d)}{B(c,d)} h(a,b,c+1,d) $$

The numerical computation in [the original blog post](http://www.bayesianwitch.com/blog/2014/bayesian_ab_test.html) can then be replaced by the above formula.

# How to compute the formula

## Recap: Evan Miller's Closed Form Solution for $@ P(X > Y) $@

In a very nice [blog post](http://www.evanmiller.org/bayesian-ab-testing.html), Evan Miller cooked up a nice *closed form* formula for evaluating $@ P( X > Y) $@ when $@ X $@ is drawn from a [Beta distribution](http://en.wikipedia.org/wiki/Beta_distribution) with integer parameters $@ (a,b) $@ and $@ Y $@ is drawn from a Beta distribution with integer parameters $@ (c,d)$@.

Expressed as an integral, we have that:

$$ P(X > y) = \int_{0}^{1} \int_{y}^{1} \frac{x^{a}(1-x)^{b}}{B(a,b)} \frac{y^{c}(1-y)^{d}}{B(c,d)} dx dy $$

Evan Miller computed the integral and came up with a closed form solution for it:

$$ P(X > Y) = 1 - \sum_{j=0}^{c-1} \frac{B(a+j,b+d) }{(d+j)B(1+j,d)B(a,b) } \equiv h(a,b,c,d) $$

## Computing the loss function

We can bootstrap this analysis and compute the loss function. We start by distributing across $@ (y-x) $@:

$$ \int_0^1 \int_y^1 (x-y) \frac{x^a(1-x)^b}{B(a,b)} \frac{y^c(1-y)^d}{B(c,d)} dx dy = $$
$$ \int_0^1 \int_y^1 \frac{x^{a+1}(1-x)^b}{B(a,b)} \frac{y^{c}(1-y)^d}{B(c,d)} dx dy - \int_0^1 \int_y^1 \frac{x^a(1-x)^b}{B(a,b)} \frac{y^{c+1}(1-y)^d}{B(c,d)} dx dy  = $$

We then multiply by $@ B(c+1,d)/B(c+1,d)$@ and $@ B(a+1,b)/B(a+1,b)$@ and do simple arithmetic:

$$ \frac{B(a+1,b)}{B(a+1,b)} \int_0^1 \int_y^1 \frac{x^{a+1}(1-x)^b}{B(a,b)} \frac{y^{c}(1-y)^d}{B(c,d)} dx dy - \frac{B(c+1,d)}{B(c+1,d)} \int_0^1 \int_y^1 \frac{x^a(1-x)^b}{B(a,b)} \frac{y^{c+1}(1-y)^d}{B(c,d)} dx dy  = $$
$$ \frac{B(a+1,b)}{B(a,b)} \int_0^1 \int_y^1 \frac{x^{a+1}(1-x)^b}{B(a+1,b)} \frac{y^{c}(1-y)^d}{B(c,d)} dx dy - \frac{B(c+1,d)}{B(c,d)} \int_0^1 \int_y^1 \frac{x^a(1-x)^b}{B(a,b)} \frac{y^{c+1}(1-y)^d}{B(c+1,d)} dx dy = $$
$$ \frac{B(a+1,b)}{B(a,b)} h(a+1,b,c,d) - \frac{B(c+1,d)}{B(c,d)} h(a,b,c+1,d) $$

This is what we wanted to show.

**Note: The original version of this post had two sign errors. Thanks to Frank (unknown last name) for catching the mistake.**
