title: Bayesian Linear Regression (in PyMC) - a different way to think about regression
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

## Computing Posteriors with PyMC

To compute the posteriors on $@ (\alpha, \beta) $@ in Python, we first import the PyMC library:

```python
import pymc
```

We then generate our data set (since this is a simulation), or otherwise load it from an original data source:

```python
from scipy.stats import norm

k = 100 #number of data points
x_data = norm(0,1).rvs(k)
y_data = x_data + norm(0,0.35).rvs(k) + 0.5
```

We then define priors on $@ (\alpha, \beta) $@. In this case, we'll choose uniform priors on [-5,5]:

```python
alpha = pymc.Uniform('alpha', lower=-5, upper=5)
beta = pymc.Uniform('beta', lower=-5, upper=5)
```

Finally, we define our observations.

```python
x = pymc.Normal('x', mu=0,tau=1,value=x_data, observed=True)

@pymc.deterministic(plot=False)
def linear_regress(x=x, alpha=alpha, beta=beta):
    return x*alpha+beta

y = pymc.Normal('output', mu=linear_regress, value=y_data, observed=True)
```

Note that for the values `x` and `y`, we've told PyMC that these values are known quantities that we obtained from observation. Then we run to some Markov Chain Monte Carlo:

```python
model = pymc.Model([x, y, alpha, beta])
mcmc = pymc.MCMC(model)
mcmc.sample(iter=100000, burn=10000, thin=10)
```

We can then draw samples from the posteriors on alpha and beta:

![posteriors on alpha and beta](|filename|blog_media/2015/bayesian_linear_regression/alpha_beta_posteriors.png)

Unsurprisingly (given how we generated the data) the posterior for $@ \alpha $@ is clustered near $@ \alpha=1 $@ and for $@ \beta $@ near $@ \beta=0.5 $@.

We can then draw a *sample* of regression lines:

![posteriors on x](|filename|blog_media/2015/bayesian_linear_regression/scatterplot_posterior.png)

Unlike in the ordinary linear regression case, we don't get a single regression line - we get a probability distribution on the space of all such lines. The width of this posterior represents the uncertainty in our estimate.

Imagine we were to change the variable `k` to `k=10` in the beginning of the python script above. Then we would have only 10 samples (rather than 100) and we'd expect much more uncertainty. Plotting a sample of regression lines reveals this uncertainty:

![posteriors on x](|filename|blog_media/2015/bayesian_linear_regression/scatterplot_posterior2.png)

In contrast, if we had far more samples (say `k=10000`), we would have far less uncertainty in the best fit line:

![posteriors on x](|filename|blog_media/2015/bayesian_linear_regression/scatterplot_posterior3.png)

## The mathematical way

**Skip this section if you prefer code to math.**

Rather than simply setting up a somewhat overcomplicated model in PyMC, one can also set up the MCMC directly. Supposing we have a data set $@D = \{ (x_i, y_i) \}$@. Then:

$$ \textrm{posterior}(\alpha,\beta | D) = \frac{ P(D | \alpha,\beta) \textrm{prior}(\alpha,\beta) } { \textrm{Const} } $$

If the samples are [i.i.d](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables), we can write this as:

$$ \textrm{posterior}(\alpha,\beta | D) = \textrm{Const} \times \textrm{prior}(\alpha,\beta) \prod_{i=1}^k P(y_i|x_i,\alpha,\beta) $$

Because we assumed the error term has a PDF and is additive, we can simplify this to:

$$ \textrm{posterior}(\alpha, \beta | D) = \textrm{Const} \times \textrm{prior}(\alpha, \beta) \prod_{i=1}^k E(y_i - \alpha \cdot x_i - \beta) $$

Given this formulation, we have now expressed the posterior as being proportional to a known function. This allows us to run any reasonable Markov Chain Monte Carlo algorithm directly and draw samples from the posterior.

# Maximal likelihood - how to do ordinary least squares

Suppose we now choose a very particular distribution - suppose we take $@ E(t) = C e^{-t^2/2} $@. Further, suppose take an [uninformative (and improper) prior](https://en.wikipedia.org/wiki/Prior_probability#Uninformative_priors), namely $@ \textrm{prior}(\alpha) = 1 $@ - this means we have literally no information on $@ \alpha $@ before we start. In this case:

$$ \textrm{posterior}(\alpha | D) = \textrm{Const} \prod_{i=1}^k \exp\left(-(y_i - \alpha \cdot x_i\right)^2/2) $$

If we attempt to maximize this quantity (or it's log) in order to find the point of maximum likelihood, we obtain the problem:

$$ \textrm{maximize} \left[ \ln\left( \textrm{Const} \prod_{i=1}^k \exp\left(-(y_i - \alpha \cdot x_i\right)^2/2) \right) \right] = $$

$$ \textrm{maximize} \left[ \textrm{Const}  \sum_{i=1}^k -(y_i - \alpha \cdot x_i)^2/2 \right]$$

This is precisely the problem of minimizing the squared error. So an uninformative prior combined with a Gaussian error term allows Bayesian Linear Regression to revert to ordinary least squares.

# Handling outliers

Ordinary least squares is notoriously bad at dealing with data having outliers.
