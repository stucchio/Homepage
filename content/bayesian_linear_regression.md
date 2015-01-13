title: Bayesian Linear Analysis - another way to think about linear regression
date: 2015-01-19 09:30
author: Chris Stucchio
tags: bayesian statistics, linear regression
mathjax: true


Linear regression is a common formula introduced in statistics classes - an easy way to get a best fit line. Alternately, it can be introduced in linear algebra as a way to fit a linear function to a set of points with minimal sum of squares error. In this blog post, I'm going to take a different tactic - I'm going to imagine that Bayesian statistics was invented first. Then I'm going to approach linear regression and linear analysis from this perspective, and see if it gets us anyplace interesting.

# Setting up the model

To begin with, we'll start with a set of observable inputs - $@ x_i \in \mathbb{R}^N, i=1\ldots k$@. For each input, there is also an observable output $@ y_i \in \mathbb{R}, i=1\ldots k $@. The general philosophy we want to propose is that we want to predict the output as accurately as possible given a set of prediction coefficients. If we could solve the problem perfectly, we would find an $@ \alpha \in \mathbb{R}^N $@ so that:

$$ \alpha \cdot x_i = \sum_{j=1}^N \alpha_j x_{i,j} = y_i $$

In reality of course, there will be errors. Provided $@ k > N $@, the problem is already overdetermined - except for very special sets of $@ (x_i, y_i) $@, we cannot come up with a solution. So at most the relation $@ y_i = \alpha \cdot x_i $@ must be viewed as an approximation.

Since we are Bayesians, the parameter $@ \alpha $@ is unknown - we only have a set of observations of it. For simplicity lets assume those observations are [independent and identically distributed](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables). I.e., this means that for every $@ i $@, we have that:

$$ y_i = \alpha \cdot x_i + e_i $$

where each $@ e_i $@ is a random variable with a pdf given by $@ E(t) $@.

Our goal will be to compute a *posterior* on $@ \alpha $@, i.e. a probability distribution $@ p(\alpha) $@ that represents our degree of belief that any particular $@ \alpha $@ is the "correct" one.

At this point it's useful to compare and contrast standard linear regression to the bayesian variety.

In **standard linear regression**, your goal is to find a single estimator $@ \hat{\alpha} $@. Then for any unknown $@ x $@, you get a point predictor $@ y_{approx} = \hat{\alpha} \cdot x $@.

In **bayesian lineare regression**, you get a probability distribution representing your degree of belief as to how likely $@ \alpha $@ is. Then for any unknown $@ x $@, you get a probability distribution on $@ y $@ representing how likely $@ y $@ is. Specifically:

$$ P(y \approx Y) = \int_{\alpha \cdot x \approx Y} \textrm{posterior}(\alpha) d\alpha $$

# How to compute a bayesian estimator?

Obviously Bayes rule is used. Suppose you have a data set $@D = \{ (x_i, y_i) \}$@. Then:

$$ \textrm{posterior}(\alpha | D) = \frac{ P(D | \alpha) \textrm{prior}(\alpha) } { \textrm{Const} } $$

Now given that our samples are [i.i.d](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables), we can write this as:

$$ \textrm{posterior}(\alpha | D) = \textrm{Const} \times \textrm{prior}(\alpha) \prod_{i=1}^k P(y_i|x_i,\alpha) $$

Because we assumed the error term has a PDF, we can simplify this to:

$$ \textrm{posterior}(\alpha | D) = \textrm{Const} \times \textrm{prior}(\alpha) \prod_{i=1}^k E(y_i - \alpha \cdot x_i) $$

So now the game is afoot. We need to construct a useful prior, $@ \textrm{prior}(\alpha) $@ and a useful error distribution. The specific manner in which we do this is problem dependent, and gives us the ability to model the world more accurately.

# Maximal likelihood - how to do ordinary least squares

Suppose we now choose a very particular distribution - suppose we take $@ E(t) = C e^{-t^2/2} $@. Further, suppose take an [uninformative (and improper) prior](https://en.wikipedia.org/wiki/Prior_probability#Uninformative_priors), namely $@ \textrm{prior}(\alpha) = 1 $@ - this means we have literally no information on $@ \alpha $@ before we start. In this case:

$$ \textrm{posterior}(\alpha | D) = \textrm{Const} \prod_{i=1}^k \exp\left(-(y_i - \alpha \cdot x_i\right)^2/2) $$

If we attempt to maximize this quantity (or it's log) in order to find the point of maximum likelihood, we obtain the problem:

$$ \textrm{maximize} \left[ \ln\left( \textrm{Const} \prod_{i=1}^k \exp\left(-(y_i - \alpha \cdot x_i\right)^2/2) \right) \right] = $$

$$ \textrm{maximize} \left[ \textrm{Const}  \sum_{i=1}^k -(y_i - \alpha \cdot x_i)^2/2 \right]$$

This is precisely the problem of minimizing the squared error. So an uninformative prior combined with a Gaussian error term allows Bayesian Linear Regression to revert to ordinary least squares.

# Handling outliers

Ordinary least squares is notoriously bad at dealing with data having outliers.
