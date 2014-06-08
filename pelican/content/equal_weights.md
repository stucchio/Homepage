title: Why a pro/con list might beat your fancy machine learning algorithm
date: 2014-06-12 09:00
author: Chris Stucchio
tags: linear regression, regression, statistics, unit-weighted regression
mathjax: true

I'm currently dating two lovely women - I'll describe them by the pseudonyms Svetlana and Elise. Unfortunately they are both growing attached to me, so the time has come for me to make a choice between them. In order to make such a choice, I wish to construct an approximation to my long term happiness - a function $@ f : \textrm{Women} \rightarrow \mathbb{R} $@ which approximately predicts my happiness with a given choice. I can then compute $@ f(\textrm{Svetlana}) $@ and $@ f(\textrm{Elise}) $@ and choose whichever one is larger - if my approximation is well chosen I will make the *utility* maximizing choice most of the time.

In statistics we have many techniques for computing such a function, [linear regression](http://en.wikipedia.org/wiki/Linear_regression) being a simple example. Unfortunately, linear regression is relatively useless to me in this case - linear regression requires a considerable number of samples, and I have not dated sufficiently many women nor kept careful records of my happiness.

Instead, I'm going to discuss a much simpler predictor, first described in [1772 by Benjamin Franklin](http://www.procon.org/view.background-resource.php?resourceID=1474). The mathematical name for it is [unit weighted regression](http://en.wikipedia.org/wiki/Unit-weighted_regression), and the practical name for it is a list of pros and cons:

<table>
<tr><th>Characteristic</th><th>Elise</th><th>Svetlana</th></tr>
<tr><td>Smart</td><td>0</td><td>+1</td></tr>
<tr><td>Great Legs</td><td>+1</td><td>+1</td></tr>
<tr><td>Black</td><td>+1</td><td>0</td></tr>
<tr><td>Rational</td><td>0</td><td>0</td></tr>
<tr><td>Exciting</td><td>+1</td><td>0</td></tr>
<tr><td>Not Fat</td><td>+1</td><td>+1</td></tr>
<tr><td>Lets me work</td><td>0</td><td>0</td></tr>
</table>



Technically that's only a list of pros - I'm treating the negation of a Con as a Pro.

Unit-weighted regression consists of taking the values in each column and adding them up. Each value is either zero or one. The net result is that $@ f(\textrm{Elise}) = 4 $@ and $@ f(\textrm{Svetlana}) = 3 $@. Elise it is!

# Unit-weighted regression is easy

One of the clearest benefits of unit-weighted regression is how easy it is for an expert to formulate a model. As an expert in my own personal choices, I am confident that I enjoy women from Africa more than women from Eastern Europe, intelligent women more than stupid ones, and that I enjoy being allowed to work without interruption. I am not confident I can apply proper weights to these facts, but I am confident they are all positive and significant.

Another important benefit is that unit weighted regression has far fewer degrees of freedom than most other regression models. The only relevant choice when building a unit-weighted regression model is what values to include and what sign to include them with. The general rule of thumb is that if a variable's sign is questionable it should be excluded from the model.

An obvious question is why I would use *unit* weighted regression rather than *linear* regression - perhaps fitting a least squares model to available data. The reason for that is simply sample size. Consider the example above - I have not dated sufficiently many women to robustly fit a 7-dimensional linear model to the available data. Additionally, I have not kept sufficiently accurate records even with this smaller sample size.

# A simple model of regression

Mathematically, a method of studying the usefuless of unit-weighted regression is to compare how accurately unit-weighted regression works relative to a more accurate predictor. Toward that end, let us consider another predictor, simple linear regression.

Let each possible choice be a a binary vector $@ \vec{x} \in \{ 0, 1 \} $@. As per our example above:

$$ \vec{\textrm{Elise}} = [ 0, 1, 1, 0, 1, 1, 0] $$

Let the true (but unknown) ranking function be $@ h(\vec{x}) = \vec{h} \cdot \vec{x} $@. For simplicity, suppose that $@ \vec{h} $@ is normalized:

$$ \sum_{i} | \vec{h}_i | = 1.0 $$

Further, suppose that we got the signs right:

$$ \forall i,  \vec{h}_i \geq 0 $$

In 3 dimensions, what this means is that the vector $@ \vec{h} $@ lives somewhere in the *2-simplex*:

![2-simplex in r^3](/blog_media/2014/equal_weights/2D-simplex.png)

In higher dimensions it is of course impossible to draw a picture, but there is a similar shape on which the vector $@ \vec{h} $@ can be contained.

The question we want to answer is the following. Consider two typical feature vectors, $@ \vec{x} $@ and $@ \vec{y} $@. How frequently does it happen that

$$ \vec{u} \cdot \vec{x} > \vec{u} \cdot \vec{y} $$

but

$$ \vec{h} \cdot \vec{x} < \vec{h} \cdot \vec{y} \textrm{?} $$

I.e., how often does the true ranking (determined by $@ \vec{h} $@) differ from the *approximate* ranking (determined by $@ \vec{u} $@)?

Equivalently, we can write this condition as:

$$ \vec{u} \cdot (\vec{x}-\vec{y}) > 0 $$

but

$$ \vec{h} \cdot (\vec{x}-\vec{y}) < 0 $$

# Monte Carlo simulation

The most obvious way to answer this question is via a computer simulation. To model the problem, I assumed the true vector $@ \vec{h} $@ was drawn from a [Dirichlet Distribution](http://en.wikipedia.org/wiki/Dirichlet_distribution) with parameters $@ [1, 1, ..., 1] $@ - i.e., essentially a uniform distribution on the unit simplex.

For each true vector, I then randomly generated vectors $@ \vec{x} $@ and $@ \vec{y} $@ by the rule $@ \vec{x}_i = 1 $@ with probability $@ 1/2 $@, otherwise $@ \vec{x}_i=0 $@ (and similarly for $@ \vec{y} $@). The result is plotted below.

![distribution of errors](/blog_media/2014/equal_weights/equal_weight_ranking_errors.png)

[Code is available](https://gist.github.com/stucchio/f5d0455fa58a4c733eba).

The graph suggests a theorem - under the assumptions above, the probability of unit-weighted regression and true linear regression yielding the same result is at least 3/4.

# Mathematical analysis

Let us consider a very simple, 3-dimensional example to build some intuition. In this example, $@ \vec{h} = [ 0.9, 0.05, 0.05] $@ - a bit of an extreme case, but reasonable. In this example, what sorts of vectors $@ \vec{x}, \vec{y} $@ will result in unit-weighted regression disagreeing with the true ranking? Here is one example:

$$ \vec{x} = [1,0,0] $$

$$ \vec{y} = [0,1,1] $$

In this case, $@ \vec{h} \cdot (\vec{x} - \vec{y}) = 0.8 $@ wereas $@ \vec{u} \cdot (\vec{x} - \vec{y}) = -1/3 $@.

Intuitively, what is happening here is that the vector $@ \vec{x} $@ is pointing nearly in the same direction as $@ \vec{h} $@, while the vector $@ \vec{y} $@ is nearly perpendicular to it.

## L1-Linf bounds

Suppose the vector $@ \vec{h} $@ satisfies $@ | \vec{h} |_\infty = a > 1/K $@. This implies that for at least one $@ i $@, $@ \vec{h}_i = a $@.

## More general analysis

To begin with, let us define the variable $@ \vec{d} = \vec{x} - \vec{y} $@. In our model, the vector $@ \vec{d} $@ is a binary vector for which $@ \vec{d}_i = -1 $@ with $@ p = 0.25 $@, $@ \vec{d}_i = 0 $@ with $@ p = 0.5 $@ and $@ \vec{d}_i = +1 $@ with $@ p = 0.25 $@.

Let us also define the variables $@ \vec{h}^+_i = \vec{h}_i$@ to be equal to $@ \vec{h} $@ on the indices for which $@ \vec{h}_i > \vec{u}_i $@ and 0 otherwise. Similarly, define $@ \vec{h}^- $@ to be the same, but on the indices where $@ \vec{h}_i \leq \vec{u}_i $@.

Define $@ \vec{d}^+, \vec{d}^- $@ similarly, but choose the indices *based on the sign of $@ \vec{h} $@.

Let us also define $@ a $@ to be the *number* of components where $@ \vec{h}^+ $@ is nonzero, and $@ b $@ to be the number of components where $@ \vec{h}^-$@ is nonzero.

**Example:** Suppose $@ \vec{h} = [0.9, 0.1, 0.1] $@ and $@ \vec{u} = [1/3, 1/3, 1/3] $@. Then $@ \vec{h}^+ = [0.9, 0, 0] $@ and $@ \vec{h}^- = [0, 0.1, 0.1] $@. If $@ \vec{d} = [1, 1, 1] $@ then $@ \vec{d}^+ = [1, 0, 0] $@ and $@ \vec{d}^- = [0,1,1] $@.

Now in the general case, $@ \vec{d}^+$@ and $@ \vec{d}^-$@ are independent random variables. We can first compute:

$$ \vec{u} \cdot \vec{d}^+ \sim B(a, 1/2) $$

and

$$ \vec{u} \cdot \vec{d}^- \sim - B(b, 1/2) $$

where $@ B(n, p) $@ represents a [binomial distribution](http://en.wikipedia.org/wiki/Binomial_distribution).

## The Corners are the problem

The answer to that question is when $@ \vec{y} $@ lives near the corner of the simplex. Consider a simple example in 3 dimensions:

$$ \vec{u} = [1/3, 1/3, 1/3] $$

$$ \vec{y} = [1, 0, 0] $$

Now consider an example vector $@ \vec{x} = [0,1,1] $@. In this case, $@ h(\vec{x}) = 0 $@ whereas $@ f(\vec{x}) = 2/3 $@.

The vector $@ \vec{u} $@ is always a vector located dead-center in the middle of the simplex.

## With lots of features, the corners take up little space

Now let us ask the question - what is a "typical" value of $@ \vec{y} $@? One way to answer this question is to take a uniform distribution on the simplex, which is equivalent to a [Dirichlet distribution](http://en.wikipedia.org/wiki/Dirichlet_distribution) with $@ \alpha_i = 1 $@. This means that all points on the simplex can occur with equal probability.

The first question we'd like to answer is what is the *expected* difference between $@ \vec{u} $@ and $@ \vec{y} $@? This can be computed straightforwardly:

$$ \int | \vec{y} - \vec{u} |^2 d\vec{y} = \sum_{i=1}^K \int | \vec{y}_i - 1/K |^2 d\vec{y} = \frac{K(K-1)}{K^2(K+1)} \sim \frac{1}{K} $$

The latter fact comes simply by applying the definition of the variance of the [Dirichlet Distribution](http://en.wikipedia.org/wiki/Dirichlet_distribution) $@ K $@ times, and noting that $@ E[\vec{y}_i] = 1/K $@. We can then compute the probability of making a significant error via the [Chebyshev Inequality](http://en.wikipedia.org/wiki/Chebyshev%27s_inequality):

$$ P( | \vec{y} - \vec{u} | > t ) \leq \frac{1}{t^2} \int | \vec{y} - \vec{u} |^2 d\vec{y} = \frac{(K-1)}{t^2 K(K+1)} \sim \frac{1}{K t^2}$$

As $@ K $@ becomes larger, this probability becomes smaller.
