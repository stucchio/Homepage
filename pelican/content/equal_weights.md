title: Why a pro/con list might beat your fancy machine learning algorithm
date: 2014-06-12 09:00
author: Chris Stucchio
tags: linear regression, regression, statistics, unit-weighted regression
mathjax: true

I'm currently dating two lovely women, Svetlana and Elise. Unfortunately continuing to date both of them is unsustainable so I must choose one. In order to make such a choice, I wish to construct an approximation to my long term happiness - a function $@ f : \textrm{Women} \rightarrow \mathbb{R} $@ which approximately predicts my happiness with a given choice. I can then compute $@ f(\textrm{Svetlana}) $@ and $@ f(\textrm{Elise}) $@ and choose whichever one is larger - if my approximation is well chosen I will make the *utility* maximizing choice most of the time.

In statistics we have many techniques for computing such a function, [linear regression](http://en.wikipedia.org/wiki/Linear_regression) being a simple example. Unfortunately, linear regression is relatively useless to me in this case - linear regression requires a considerable number of samples, and I have not dated sufficiently many women nor kept careful records of my happiness.

Instead, I'm going to discuss a much simpler method of making decisions, described in [1772 by Benjamin Franklin](http://www.procon.org/view.background-resource.php?resourceID=1474):

> ...my Way is, to divide half a Sheet of Paper by a Line into two Columns, writing over the one Pro, and over the other Con. Then...I put down under the different Heads short Hints of the different Motives...I find at length where the Ballance lies...I come to a Determination accordingly.

The mathematical name for it is [unit weighted regression](http://en.wikipedia.org/wiki/Unit-weighted_regression). I present the method in a slightly different format - in each column a different choice is listed. Each row represents a characteristic, all of which are pros. A con is transformed into a pro by negation - rather than treating "disturbs my work" as a con, I treat "Lets me work" as a pro.

If a woman posesses the characteristic under discussion, a +1 is assigned to the relevant row/column, otherwise 0 is assigned:

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

Unit-weighted regression consists of taking the values in each column and adding them up. Each value is either zero or one. The net result is that $@ f(\textrm{Elise}) = 4 $@ and $@ f(\textrm{Svetlana}) = 3 $@. Elise it is!

# Pro/Con lists are easy

A pro/con list is one of the simplest ranking algorithms you can construct. The mathematical sophistication required is grade school arithmetic and it's so easy to program that even a RoR hipster could do it. As a result, you should not hesitate to implement a pro/con list for decision processes.

The key factor in the success of unit-weighted regression is feature selection. The rule of thumb here is very simple - choose features which you have good reason to believe are strongly predictive of the quantity you wish to rank. Such features can usually be determined without a lot of data - typically a combination of expert opinion and easy correlations are sufficient. For example, I do not need a large amount of data to determine that I consider "not fat" to be a positive predictor of my happiness with a woman.

Conversely, if the predictiveness of a feature is not clear, it should not be used.

## Linear regression is hard

An obvious question the reader might ask is why I would ever use unit-weighted regression, as opposed to the more general *linear* regression predictor. Linear regression is a lot like a pro/con list, except that the weight of each feature is allowed to vary. In mathematical terms, we represent each possible choice as a binary vector - for example:

$$ \vec{\textrm{Elise}} = [ 0, 1, 1, 0, 1, 1, 0] $$

Then the predictor function uses a set of weights which can take on values other than $@ +1 $@:

$$ f(\vec{x}) = \sum_i h_i x_i $$

The individual weights $@ f_i $@ represent how important each variable is. For example, "Smart" might receive a weight of +3.3, "Not fat" a weight of +3.1 and "Black" a weight of +0.9.

The weights can be determined with a reasonable degree of accuracy by taking past data and choosing the weights which minimize the difference between the "true" value and the approximate value - this is what [least squares](http://en.wikipedia.org/wiki/Least_squares) does.

Fitting a linear model only works when you have sufficient data. To robustly fit a linear model, you'll need tens to hundreds of data points *per feature*. If you have too few data points, you run into a real danger of overfitting - building a model which accurately memorizes the past, but fails to predict the future. You can even run into this problem if you have lots of data points, but those data points don't represent all the features in question.

It also requires more mathematical and programming sophistication to build.

In principle fitting a linear model to the data is the right way to go. After all, in real life, some factors are 3x or 10x more important than others. But in practice, it can be difficult to do it right.

# How well does it work?

This is where things get interesting. It turns out that Pro/Con list is at least 75% as good as a linear regression model.

Suppose we've done linear regression and found linear regression coefficients $@ \vec{h} $@. Suppose instead of using the vector $@ \vec{h} $@, we instead used the vector of unit weights, $@ \vec{u} = [ 1/N, 1/N, \ldots, 1/N] $@. Here $@ N $@ is the number of features in the model.

An error is made whenever the pro/con list and linear regression rank two vectors differently - i.e., linear regression says "choose Elise" while the pro/con list says "choose Svetlana". The *error rate* of the pro/con list is the probability of making an error given two random *feature vectors* $@ \vec{x} $@ and $@ \vec{y} $@, i.e.:

$$ \textrm{error rate} = P( \textrm{sign}( [\vec{h} \cdot (\vec{x} - \vec{y})] [\vec{u} \cdot (\vec{x} - \vec{y})] ) < 0 ) $$

It turns out that if you average it out over all vectors $@ \vec{h} $@, the error rate is bounded by 1/4. There are of course vectors $@ \vec{h} $@ for which the error rate is higher, and others for which it is lower. But on average, the error rate is bounded by 1/4.

In this sense, the pro/con list is 75% as good as linear regression.

We can confirm this fact by computer simulation - generating a random ensemble of vectors $@ \vec{h} $@, and then measuring how accurately unit-weighted regression agrees with it. The result:

![distribution of errors](/blog_media/2014/equal_weights/equal_weight_ranking_errors.png)

[Code is available](https://gist.github.com/stucchio/f5d0455fa58a4c733eba).

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

## Normally distributed feature vectors

Suppose for simplicity that the feature vectors $@ \vec{x}, \vec{y} $@ satisfy $@ \vec{x}_i \sim N(0,2^{-1/2}) $@. Define $@ \vec{d} = \vec{x} - \vec{y} $@, and note that $@ \vec{d}_i \sim N(0,1) $@. This is an unrealistic assumption, but one which is mathematically tractable. We want to compute the probability:

$$ P( (\vec{h} \cdot \vec{d} > 0 \textrm{ and } \vec{u} \cdot \vec{d} < 0) \textrm{ or } (\vec{h} \cdot \vec{d} < 0 \textrm{ and } \vec{u} \cdot \vec{d} > 0) ) $$
$$ = 2 P( (\vec{h} \cdot \vec{d} > 0 \textrm{ and } \vec{u} \cdot \vec{d} < 0) ). $$

For simplicity, we will attempt to compute the latter quantity.

### How accurately does $@ \vec{u} $@ approximate $@ \vec{h} $@?

Define $@ \vec{h} = \vec{u} + \vec{p} $@ where $@ \vec{p} \cdot \vec{u} = 0 $@. Then:

$$ P( \vec{h} \cdot \vec{d} > 0 \textrm{ and } \vec{u} \cdot \vec{d} < 0 ) $$

$$ = P( \vec{u} \cdot \vec{d} + \vec{p} \cdot \vec{d} > 0 \textrm{ and } \vec{u} \cdot \vec{d} < 0 ) $$

$$ = P( \vec{p} \cdot \vec{d} > - \vec{u} \cdot \vec{d} \textrm{ and } \vec{u} \cdot \vec{d} < 0 ) $$

Note that $@ \vec{d} $@ is generated by a multivariate normal distribution, with covariance matrix equal to the identity. As a result:

$$ \vec{u} \cdot \vec{d} \sim N(0, N^{-1} ) $$

where $@ N $@ is the dimension of the problem. Similarly:

$$ \vec{p} \cdot \vec{d} \sim N\left(0, \sum \vec{p}_i^2 \right) $$

Due to the orthogonality of $@ \vec{u} $@ and $@ \vec{p} $@, the quantities $@ \vec{u} \cdot \vec{d} $@ and $@ \vec{p} \cdot \vec{d} $@ are independent.

**Note:** Obtaining this statistical independence is why we needed to assume the feature vectors were normal - showing statistical independence in the case of binary vectors is harder. A potentially easier test case than binary vectors might be random vectors chosen uniformly from the unit ball in $@ l^\infty $@, aka vectors for which  $@ \max_i |\vec{x}_i| < 1$@.

We've now reduced the problem to simple calculus. Define $@ \sigma_u^2 = N^{-1} $@ and $@ \sigma_p^2 = \sum \vec{p}_i^2 $@. Let $@ v = \vec{u} \cdot \vec{d} $@ and $@ w = \vec{p} \cdot \vec{d} $@. Then:

$$ P( (\vec{h} \cdot \vec{d} > 0 \textrm{ and } \vec{u} \cdot \vec{d} < 0) ) = \int_{-\infty}^0 \int_{-v}^{\infty} C \exp\left(\frac{-v^2}{2\sigma_u^2} + \frac{-w^2}{2\sigma_p^2} \right) dw dv $$

Changing variables to $@ v = r \sigma_u \cos(\theta) $@, $@ w = r \sigma_p \sin(\theta) $@. Then:

$$ \int_{-\infty}^0 \int_{-v}^{\infty} C \exp\left(\frac{-v^2}{2\sigma_u^2} + \frac{-w^2}{2\sigma_p^2} \right) dw dv = \int_{\theta_0}^{\pi/2} \int_0^\infty C' e^{-r^2} r dr d\theta = \frac{\theta_0-\pi/2}{2\pi}$$

Here $@ \theta_0 = \textrm{arccot}(\sigma_u/\sigma_p) $@, so:

$$ P( (\vec{h} \cdot \vec{d} > 0 \textrm{ and } \vec{u} \cdot \vec{d} < 0) ) = \frac{ \pi/2 - \textrm{arccot}(\sigma_p/\sigma_u)}{2\pi} = \frac{ \arctan(\sigma_p/\sigma_u)}{2\pi} = \frac{ \arctan(\sqrt{N} \sigma_p)}{2\pi} $$

### Worse case analysis

The worst case to consider is when $@ \vec{h}$@ is one of the corners of the unit simplex - e.g. $@ \vec{h} = [1,0,\ldots,0] $@. In this case:

$$ | \vec{p} |^2 = |\vec{h}-\vec{u}|^2 - = \frac{N-1}{N} = \sigma_p^2 $$

So $@ \sigma_p = \sqrt{(N-1)/N} $@ while $@ \sigma_u = 1/\sqrt{N} $@, and $@ \textrm{arccot}( -1/\sqrt{N-1} ) \rightarrow \pi $@ as $@ N \rightarrow \infty $@. This implies:

$$ P( (\vec{h} \cdot \vec{d} > 0 \textrm{ and } \vec{u} \cdot \vec{d} < 0) ) = \frac{ \arctan(\sqrt{N-1})}{2\pi} \rightarrow \frac{1}{4} $$

This means that in the worst case, unit-weighted regression is no better than chance.

### Average case analysis

Let us now consider the *average* case over all vectors $@ \vec{h} $@. To handle this case, we must impose a probability distribution on such vectors. The natural distribution to consider is the uniform distribution on the unit-simplex, which is equivalent to a [Dirichlet](http://en.wikipedia.org/wiki/Dirichlet_distribution) distribution with $@ \alpha_1 = \alpha_2 = \ldots = \alpha_N = 1 $@.

So what we want to compute is:

$$ E[P( (\vec{h} \cdot \vec{d} > 0 \textrm{ and } \vec{u} \cdot \vec{d} < 0) )] = \int P( (\vec{h} \cdot \vec{d} > 0 \textrm{ and } \vec{u} \cdot \vec{d} < 0) ) d\vec{h} $$

This can be bounded above as follows, noting that $@ \sigma_p = \sqrt{| \vec{h} - \vec{u}|^2} $@:

$$ \int P( (\vec{h} \cdot \vec{d} > 0 \textrm{ and } \vec{u} \cdot \vec{d} < 0) ) d\vec{h} = \int \frac{ \arctan(\sqrt{N} \sqrt{| \vec{h} - \vec{u}|^2})}{2\pi} d\vec{h} $$
$$ \leq \frac{ \arctan( \sqrt{N} \sqrt{ \int | \vec{h} - \vec{u}|^2 d\vec{h} } ) }{2\pi} = \frac{ \arctan( \sqrt{N} \sqrt{ (N-1)/(N(N+1)) } ) }{2\pi} $$
$$ = \frac{ \arctan( \sqrt{ (N-1)/(N+1) } ) }{2\pi} $$

The inequality follows from [Jensen's Inequality](http://en.wikipedia.org/wiki/Jensen's_inequality) since $@ z \mapsto \arctan(\sqrt{N} \sqrt{z}) $@ is a concave function.

For large $@ N $@ this quantity approaches $@ \arctan(1) / 2 \pi = (\pi/4) / (2\pi) = 1/8 $@.

Thus, we have shown that the average error-rate of unit-weighted regression is bounded above by $@ 1/4 $@. A monte carlo simulation confirms that the theoretical bound appears correct. It also shows that treating feature vectors as Gaussian rather than Boolean vectors appears to be a reasonable approximation to the problem - if anything it introduces extra error.

![average case, theory vs practice](/blog_media/2014/equal_weights/theory_vs_practice.png)

Code to produce the graph [is available on github](https://gist.github.com/stucchio/142620be989dcf2767bc).

**Note:** The reason the Bernoulli feature vectors appear to have lower error than the Gaussian feature vectors for small N appears to be caused by the fact that for small N, there is a significant possibility that a feature vector might be 0 in the important components. The net result of this is that $@ \vec{h} \cdot (\vec{x} - \vec{y}) = 0 $@ fairly often, meaning that many vectors have equal rank. This effect becomes improbable as more features are introduced.
