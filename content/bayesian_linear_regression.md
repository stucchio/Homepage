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

Our goal will be to compute a *posterior* on $@ \alpha $@, i.e. a probability distribution $@ p(\alpha) $@ that represents our degree of belief that any particular $@ \alpha $@ is the best one.

If you think about it, that's rather different from the normal case of linear regression.
