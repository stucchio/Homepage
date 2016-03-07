title: Has your conversion rate changed? An introduction to Bayesian timeseries analysis with Python.
date: 2016-3-08 08:45
author: Chris Stucchio
tags: statistics, bayesian reasoning
mathjax: true
category: conversion rate optimization


When running a large site, it's important to monitor site behavior. For an ecommerce or similar site, the key thing to measure is conversion rate - if your conversion rate goes down, something is wrong. A common - but *wrong* - way to measure conversion rate is to simply use a rolling window. If the desired conversion rate is 5%, one might plot the conversion rate over the past 1 hour and trigger an alert if the conversion rate drops below some threshold.

Unfortunately, as Willie Wheeler observes in his blog post [Monitoring Bookings and the Law of Large Numbers](http://williewheeler.com/2015/05/16/monitoring-bookings-and-the-law-of-large-numbers/), a static threshold simply doesn't work. The problem is that variation in the number of *visitors* over time changes and a reduced number of visitors will increase the variance of your conversion rate. Consider the following scenario - a uniform 5% conversion rate. During some time periods the number of visitors is 10,000, while during others it's only 1,000.

Supose we were to raise an alert whenever the empirical conversion rate dropped below 4%. In this case, the false positive rate during periods when there are 10,000 visitors would be only `binom(10000, 0.05).cdf(400) == 1.21e-06`. That's pretty good! However, during the low traffic periods, that false positive rate rises to `binom(1000, 0.05).cdf(40) = 0.081`. Whoops!

In pictures, here's what happens:

![increased variance](/blog_media/2016/has_your_conversion_rate_changed/law_of_large_numbers.png)

Based on this analysis it's pretty clear no static threshold can be used. However, we can use

This problem can be resolved by a Bayesian timeseries model.

## Bayesian Timeseries Analysis

A timeseries is simply a function of time - $@ f: \mathbb{R} \rightarrow T $@. Bayesian timeseries analysis is simply the discipline of using Bayesian statistics to study functions which vary (possibly stochastically) with time. As an example, lets consider how the problem of monitoring conversion rate over time can be framed as a statistics problem.

Here's the basic idea. Let us allow $@ \theta(t) $@ to reprsent our conversion rate as a function of time. As an oversimplified model, lets assume $@ \theta(t) $@ takes the following form. First of all, at $@ t = 0 $@, $@ \theta(t) = p_0 $@. As time progresses, the conversion rate can change instantaneously at a known average rate $@ \lambda $@ per unit time. Supposing the conversion rate changes at time $@ t_1 $@, it will change to a new rate $@ p_1 $@ drawn from a known distribution $@ f(p) $@.

So in simple terms:

$$
\theta(t) = p_0, t \leq t_1
$$
$$
\theta(t) = p_1, t > t_1
$$
$$
p_1 \leftarrow f(p)
$$

Since this jump happens at a known constant rate, it can be represented with a Poisson distribution. Thus, the probability that $@ t_1 > T $@ is $@ e^{-\lambda T} $@.

If we could measure $@ \theta(t) $@ directly, it would be straightforward to identify $@p_0$@, $@p_1$@ and $@ t_1 $@. And if we have enough data (say 10,000 data points per unit of time), we can easily observe this:

![increased variance](/blog_media/2016/has_your_conversion_rate_changed/lots_of_data_timeseris.png)

But when the number of data points we have is lower - say 1,000 per unit time - it's harder to observe a jump.

![increased variance](/blog_media/2016/has_your_conversion_rate_changed/less_data_timeseris.png)

How can we extract the maximal amount of information from the data available?

## Computing the likelihood of a timeseries

Consider a timeseries $@ \theta(t) $@. Suppose we've made an observation - at time $@ t $@ there were $@ n_t $@ visitors and $@ c_t $@ conversions. What is the likelihood that this occurred?

The likelihood is defined as $@ P(c_t | \theta(t), n_t) $@. It's the probability of seeing the result we just saw, given some value of the unknown parameter. Luckily this question is easily answered with the Binomial theorem:

$$
P(c_t | \theta(t), n_t) = {n_t \choose c_t } \theta(t)^{c_t}(1-\theta(t))^{n_t - c_t}
$$

Now given a data series - a sequence of points $@ (n_1, c_1), (n_2, c_2), \ldots $@, we can compute the likelihood of observing this series:

$$
P(c_1, c_2, \ldots | \theta(t), n_1, n_2, \ldots) = \prod_i {n_i \choose c_i } \theta(i)^{c_i}(1-\theta(t))^{n_i - c_i}
$$

Sometimes more usefully, we might wish to consider the log likelihood:

$$
\log\left[ P(c_1, c_2, \ldots | \theta(t), n_1, n_2, \ldots) ]\right] = \sum_i \log\left[ {n_i \choose c_i } \right] \left( c_i \log(\theta(i)) (n_i - c_i)\log(1-\theta(t)) \right)
$$


### Computing the likelihood with Python

Suppose now we have input data - a timeseries `n` and `c` representing visitor count and conversions:

```
n = array([ 1000.,  1000.,  1000.,  1000.,  1000.,  1000.,  1000.,  1000.,
            1000.,  1000.,  1000.,  1000.,  1000.,  1000.,  1000.,  1000.,
            1000.,  1000.,  1000.,  1000.])

c = array([51, 40, 51, 41, 44, 39, 54, 41, 61, 52, 65, 58, 44, 49, 34, 39, 24,
           28, 36, 43])
```

Then let us represent `theta` with an array as well.

```
theta = array([ 0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,
                0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,
                0.05,  0.05])
```

The log likelihood can be computed via:

```
def log_likelihood(n, c, theta):
    return sum(binom.logpmf(c, n, theta))
```

And of course the likelihood itself can be computed via:

```
def likelihood(n, c, theta):
    return exp(log_likelihood(n,c,theta))
```


### Comparing likelihoods

Now let us imagine we had two alternate theories about what $@ \theta(t) $@ might be. Consider our first hypothesis - a sort of a "null hypothesis" - as the theory that the conversion rate has remained constant:

$$
\theta^0(t) = 0.05
$$

Now consider an "alternate hypothesis" - the assumption that the conversion rate dropped from 5% to 3% at time 14.

$$\theta^{14}(t) = 0.05, t \leq 14 $$
$$\theta^{14}(t) = 0.03, t > 14 $$

This is a very specific alternate hypothesis, but this process is done mainly for illustrative purposes.

(I put "null hypothesis" and "alternate hypothesis" in scare quotes since I'm not planning on using them in a Frequentist manner.)

Using the likelihood formula for $@ P(c_1, c_2, \ldots | \theta(t), n_1, n_2, \ldots) $@ above, we find that:

$$ \log \left[ P(c_1, c_2, \ldots | \theta^0(t), n_1, n_2, \ldots) \right] = -86.991405224581854 $$

and

$$ \log \left[ P(c_1, c_2, \ldots | \theta^{14}(t), n_1, n_2, \ldots) \right] = -70.445464783971829 $$

(I've shifted to a log scale to make the numbers easier to observe.)

Now lets consider a range of alternate hypothesis, each representing the possibility of a jump at a different time:

$$\theta^{i}(t) = 0.05, i \leq 14 $$
$$\theta^{i}(t) = 0.03, i > 14 $$

We can plot the log likelihood of these various alternate hypothesis. The green line in this plot represents the "null hypothesis" that no jump occurred, and the conversion rate remained 5% for all time.

![increased variance](/blog_media/2016/has_your_conversion_rate_changed/log_likelihood_of_jump_time.png)

The fact that the log likelihood peaks at $@ t=14 $@ suggesting that whatever we believed before, we should hold a stronger belief that our conversion rate dropped from 5% to 3% at approximately $@ t = 14 $@.

## Bayesian Inference

Bayesian inference takes our rough intuition - that we should consider a drop in conversion rate at $@ t = 14 $@ - and quantifies it.

To do Bayesian inference, we need to come up with a prior. As a prior, I'll assume that a drop in conversion rate is unlikely - only 2%. I'll also assume that the probability of a drop occurring at any given time is equal.

For simplicity I'll assume that if a drop occurs, the drop is from 5% to 3%.

Thus, as a prior, we obtain:

$$ P(\theta^0) = 0.98 \textrm{(No drop)} $$
$$ P(\theta^1) = 0.001 \textrm{(Drop at time 1)} $$
$$ P(\theta^2) = 0.001 $$
$$ \ldots $$

To compute a posterior, we need to use Bayes rule:

$$
P(\theta^i | (n_1, c_1), (n_2, c_2), \ldots ) = \frac {
  P((n_1, c_1), (n_2, c_2), \ldots | \theta^i ) P(\theta^i)
}{
  P((n_1, c_1), (n_2, c_2), \ldots )
}
$$

So for example, we can compute the probability of there being no jump as:

$$ P(\theta^0 | (n_1, c_1), (n_2, c_2), \ldots ) = \frac {
  e^{-86.99} \cdot 0.98
}{
  P((n_1, c_1), (n_2, c_2), \ldots )
}
= 5.67 \times 10^{-5}
$$

In contrast, the probability of a jump at t=14 is:

$$ P(\theta^0 | (n_1, c_1), (n_2, c_2), \ldots ) = \frac {
  e^{-70.45} \cdot 0.001
}{
  P((n_1, c_1), (n_2, c_2), \ldots )
}
= 0.887
$$

Repeating this calculation for all times yields the following plot of the posterior on the time at which the conversion rate dropped:

![increased variance](/blog_media/2016/has_your_conversion_rate_changed/prior_posterior_jump_time.png)

We can draw the conclusion that a jump almost certainly occurred (with probability 99.95%) at some point between t=13 and t=17. This means we should raise an alert!




See also a post on [Willie Wheeler's blog](http://williewheeler.com/2016/03/03/anomaly-detection-using-stl/) where he discusses an extension of this problem - what if the base rate $@ \lambda(t) $@ varies with time.
