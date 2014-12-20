title: Asymptotics of Evan Miller's Bayesian A/B formula
date: 2014-06-09 08:30
author: Chris Stucchio
tags: ab testing, bayesian statistics, ab testing, asymptotics
mathjax: true


Earlier this year I published a blog post about a [Baysian decision rule](http://www.bayesianwitch.com/blog/2014/bayesian_ab_test.html) for choosing between two variations, each with a potentially different conversion rate. Later Evan Miller wrote a [blog post](http://www.evanmiller.org/bayesian-ab-testing.html) computing an exact formula for evaluating it, rather than approximating the integral numerically. In this post I'm going to derive an [asymptotic expansion](http://en.wikipedia.org/wiki/Asymptotic_expansion) of that formula which is valid in the limit of large sample sizes - this is the case when Evan's formula will become computationally difficult to evaluate and prone to numerical error.

# The Asymptotic Expansion

The goal is to compute the function:

$$ g(a,b,c,d) = \int_0^1 \int_y^1 \frac{x^{a-1}(1-x)^{b-1}}{B(a,b)} \frac{y^{c-1}(1-y)^{d-1}}{B(c,d)} dx dy $$

In terms of Bayesian A/B testing, this function has the definition:

$$ g(a,b,c,d) = P( \textrm{Conversion Rate of A > Conversion Rate of B}) $$

Evan Miller discovered a [formula](http://www.evanmiller.org/bayesian-ab-testing.html) for this, which is somewhat computationally intensive:

$$ g(a,b,c,d) = 1 - \sum_{j=0}^{c-1} \frac{B(a+j,b+d) }{(d+j)B(1+j,b)B(a,b) } $$

This is computationally intensive because a term in the sum must be computed for every data point. However, if we make a scaling assumption, we can derive a much simpler formula. Specifically, let us assume that $@ a-1=N\phi, b-1=N(1-\phi), c-1=N\psi, d-1=N(1-\psi) $@, with $@ N \rightarrow \infty $@. Provided $@ N $@ is sufficiently large and $@ 0 \leq \phi < \psi \leq 1$@, we have the approximate formula:

$$ g(N\phi+1, N(1-\phi)+1, N\psi+1, N(1-\psi)+1) = \frac{ 2 B( N(\phi+\psi) + 2, N(2-\phi-\psi)+2) } { B(N\phi-1, N(1-\phi)-1) B(N\psi-1, N(1-\psi)-1) N(\psi-\phi) } \left(1 + O(N^{-1}) \right)$$

The function $@ B(a,b) $@ is the standard [Beta function](http://en.wikipedia.org/wiki/Beta_function).

For those unfamiliar with asymptotics, the formula means the following. Suppose we approximate

$$ g(N\phi+1, N(1-\phi)+1, N\psi+1, N(1-\psi)+1) $$

by

$$ \frac{ 2 B( N(\phi+\psi) + 2, N(2-\phi-\psi)+2) } { B(N\phi-1, N(1-\phi)-1) B(N\psi-1, N(1-\psi)-1) N(\psi-\phi) }. $$

Then the error (expressed as a percentage of the true value) will decay at the rate $@ O(1/N) $@. This can be quantified more precisely, but I don't feel like computing error bounds right now.

If we graph the relative error (namely $@ (\textrm{asymptotic} / \textrm{exact} - 1) $@), we observe the expected behavior:

![graph of asymptotic error](/blog_media/2014/bayesian_asymptotics/asymptotic_errors.png)

The graph was generated with the following [Julia script](https://gist.github.com/stucchio/1a0abf880eb332175c02).

## Problems with this method

One flaw with the method described here is that it insists both variants of the A/B test be displayed to the *exact* same number of users. It is my belief that this assumption can be relaxed. We would instead take the scaling law:

$$ a-1=N\phi, b-1=N(1-\phi) $$

$$ c-1=\alpha N\psi, d-1=\alpha N(1-\psi) $$

Here $@ \alpha \approx 1 $@, meaning that the two variations no longer need to have the *exact* same number of users.

**Conjecture:** The method described here can be made to work with this scaling, and the only result will be minor changes in the formula, of the form $@ \psi \mapsto \alpha \psi $@ and $@ (2-\phi-\psi) \mapsto 1+\alpha-\phi-\alpha\psi $@.

# Here comes the math

For any reader unfamiliar with Laplace's method and asymptotic analysis, you can read this [free pdf](http://www.pas.rochester.edu/~rajeev/phy493/AsymptoticMethods.pdf) on the topic. The classic (but expensive) textbook is [Asymptotics and Special Functions](http://www.amazon.com/gp/product/1568810695/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=1568810695&linkCode=as2&tag=christuc-20&linkId=2PHYJMUHXP65N6M7) by Olver.

Define $@ C = C(a,b,c,d) \equiv [ B(a,b) B(c,d) ]^{-1} $@ to simplify the notation.

Let us rewrite the integral as the integral of an exponential:

$$ C \int_0^1 \int_y^1 x^{a-1}(1-x)^{b-1} y^{c-1}(1-y)^{d-1} dx dy  $$
$$ = C \int_0^1 \int_y^1 x^{N\phi}(1-x)^{N(1-\phi)} y^{N\psi}(1-y)^{N(1-\psi)} dx dy $$
$$ = C \int_0^1 \int_y^1 \exp \left[N \left(\phi \ln(x) + (1-\phi)\ln(1-x) \right) + \psi \ln(y) + (1-\psi) \ln (1-y) \right] dx dy $$

We can then change variables to $@ u=(x-y)/2 $@ and $@ v = (x+y)/2$@. Then:

$$ = 2 C \int_0^{1} \int_0^{\min(v,1-v)}  \exp \left[N \left(\phi \ln(u+v) + (1-\phi)\ln(1-u-v) + \psi \ln(v-u) + (1-\psi) \ln (1-v+u) \right) \right] du dv $$

## Laplace's Method

At this point we will use [Laplace's Method](http://en.wikipedia.org/wiki/Laplace's_method) to compute the asymptotics of the integral.

Define the function:

$$ \eta(x,y) = \phi \ln(x) + (1-\phi)\ln(1-x) + \psi \ln(y) + (1-\psi) \ln (1-y) $$

Or equivalently:

$$ \hat{\eta}(u,v) = \phi \ln(u+v) + (1-\phi)\ln(1-u-v) + \psi \ln(v-u) + (1-\psi) \ln (1-v+u) $$

**Fact:** The unique global maxima of $@ \eta(u,v) $@ is achieved at $@ (x,y) = (\phi, \psi) $@. There are no local maxima.

The interesting case is when $@ \phi < \psi $@. This puts the maxima of $@ \eta(x,y) $@ in top left corner, whereas the region being integrated is in the lower right side. This corresponds to the case when $@ P( \textrm{version B is better than Version A}) < 1/2 $@, and we want to determine by how much it is better.

## The grunt work

If $@ \phi < \psi$@, the maxima of $@ \eta(u,v) $@ is in the top left side of the unit square, while the region of integration is the lower right side. This means that for the inner integral, the maxima of $@ \eta(x,y) $@ is achieved at the left endpoint $@ u=0 $@. Applying Laplace's method, we find:

$$ \int_0^{\min(v,1-v)} e^{N \hat{\eta}(u,v)} du = \frac{ - e^{N \hat{\eta}(0, v) } }{ N \partial_u \hat{\eta}(0,v) }\left(1 + O(N^{-1}) \right) $$

A simple computation shows that:

$$ \partial_u \hat{\eta}(0,v) = \left[ \frac{\phi}{u+v} - \frac{(1-\phi)}{1-u-v} -  \frac{\psi}{v-u} + \frac{(1-\psi)}{1-v+u} \right]_{u=0} $$
$$ = \frac{\phi - \psi}{v} + \frac{\phi-\psi}{1-v} = (\phi-\psi) \frac{1}{v(1-v)} $$

And also:

$$ \hat{\eta}(0,v) = \phi \ln(v) + (1-\phi)\ln(1-v) + \psi \ln(v) + (1-\psi) \ln (1-v) $$
$$ = (\phi + \psi) \ln(v) + (2-\phi-\psi)\ln(1-v) $$

Substituting this in, we have:

$$ \int_0^{\min(v,1-v)} e^{N \hat{\eta}(u,v)} du = \frac{ - e^{N \hat{\eta}(0, v) } }{ N \partial_v \hat{\eta}(0,v) } \left(1 + O(N^{-1}) \right) $$
$$ = \exp \left( N \left[ (\phi + \psi) \ln(v) + (2-\phi-\psi)\ln(1-v) \right] \right) \frac{v(1-v)}{N(\psi-\phi)} \left(1 + O(N^{-1}) \right) $$
$$ = \frac{ v^{N(\phi+\psi) + 1} (1-v)^{N(2-\phi-\psi)+1} }{N(\psi-\phi)} \left(1 + O(N^{-1}) \right) $$

We can now plug this formula into the definition of $@ g( N\phi, N(1-\phi), N\psi, N(1-\psi))$@:

$$ 2 C \int_0^{1} \int_0^{\min(v,1-v)}  \exp \left[N \left(\phi \ln(u+v) + (1-\phi)\ln(1-u-v) + \psi \ln(v-u) + (1-\psi) \ln (1-v+u) \right) \right] du dv $$
$$ = 2 C \int_0^{1} \frac{ v^{N(\phi+\psi) + 1} (1-v)^{N(2-\phi-\psi)+1} }{N(\psi-\phi)} \left(1 + O(N^{-1}) \right) dv $$

The reader will observe that this integral is the definition of the Beta function.

$$ = \frac{ 2 B( N(\phi+\psi) + 2, N(2-\phi-\psi)+2) } { B(N\phi-1, N(1-\phi)-1) B(N\psi-1, N(1-\psi)-1) N(\psi-\phi) } \left(1 + O(N^{-1}) \right) $$

This is what we wanted to show.

In principle higher order terms can also be computed, but that seems unnecessary at this point. I believe the approach in section 3 of [Asymptotic Inversion of the Incopmlete Beta Function](http://oai.cwi.nl/oai/asset/2294/2294A.pdf) may also be useful.
