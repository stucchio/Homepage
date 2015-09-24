title: Bayesian Linear Regression (in PyMC) - an interesting way to think
date: 2015-09-28 09:30
author: Chris Stucchio
tags: bayesian statistics, linear regression
mathjax: true

![simple regression](|filename|blog_media/2015/bayesian_linear_regression/simple_regression.png)

Consider a data set, a sequence of point $@ (x_1, y_1), (x_2, y_2), \ldots, (x_k, y_k)$@. We are interested in discovering the relationship between x and y. Linear regression, at it's simplest, assumes a relationship between x and y of the form $@ y = \alpha x + \beta + e$@. Here, the variable $@ e $@ is a *noise* term - it's a random variable that is independent of $@ x $@, and varies from observation to observation. This assumed relationship is called the *model*.

(In the case where x is a vector, the relationship is assumed to take the form $@ y = \alpha \cdot x + \beta + e$@. But we won't get into that in this post.)

The problem of linear regression is then to estimate $@ \alpha, \beta $@ and possibly $@ e $@.

In this blog post, I'll approach this problem from a Bayesian point of view. Ordinary linear regression (as taught in introductory statistics textbooks) offers a recipe which works great under a few circumstances, but has a variety of weaknesses. These weaknesses include an extreme sensitivity to outliers, an inability to incorporate priors, and little ability to quantify uncertainty.

Bayesian linear regression offers a very different way to think about things. Combined with some computation (and note - computationally it's a LOT harder than ordinary least squares), one can easily formulate and solve a very flexible model that addresses most of the problems with ordinary least squares.

# The simplest version

To begin with, let's assume we have a one-dimensional dataset $@ (x_1, y_1), \ldots, (x_k, y_k) $@. The goal is to predict $@ y_i $@ as a function of $@ x_i $@. Our model describing $@ y_i $@ is

$$ y_i = \alpha x_i + \beta + e $$

where $@ \alpha $@ and $@ \beta $@ are unknown parameters, and $@ e $@ is the statistical noise. In the Bayesian approach, $@ \alpha $@ and $@ \beta $@ are unknown, and all we can do is form an opinion (compute a posterior) about what they might be.

To start off, we'll assume that our observations are [independent and identically distributed](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables). This means that for every $@ i $@, we have that:

$$ y_i = \alpha \cdot x_i + e_i $$

where each $@ e_i $@ is a random variable. Let's assume that $@ e_i $@ is an absolutely continuous random variable, which means that it has a probability density function given by $@ E(t) $@.

Our goal will be to compute a *posterior* on $@ (\alpha, \beta) $@, i.e. a probability distribution $@ p(\alpha,\beta) $@ that represents our degree of belief that any particular $@ (\alpha,\beta) $@ is the "correct" one.

At this point it's useful to compare and contrast standard linear regression to the bayesian variety.

In **standard linear regression**, your goal is to find a single estimator $@ \hat{\alpha} $@. Then for any unknown $@ x $@, you get a point predictor $@ y_{approx} = \hat{\alpha} \cdot x $@.

In **bayesian linear regression**, you get a probability distribution representing your degree of belief as to how likely $@ \alpha $@ is. Then for any unknown $@ x $@, you get a probability distribution on $@ y $@ representing how likely $@ y $@ is. Specifically:

$$ p(y = Y) = \int_{\alpha \cdot x + \beta = Y} \textrm{posterior}(\alpha,\beta) d\alpha $$

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
