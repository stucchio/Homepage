Isotonic: A Python package for doing fancier versions of isotonic regression
############################################################################
:date: 2020-03-10 08:30
:author: Chris Stucchio
:tags: python, statistics
:featured: true


Frequently in data science, we have a relationship between :code:`X` and :code:`y` where (probabilistically) :code:`y` increases as :code:`X` does. The relationship is often not linear, but rather reflects something more complex. Here's an example of a relationship like this:

.. image:: |filename|blog_media/2020/isotonic_python_package/monotonic_relation.png

In this plot of synthetic we have a non-linear but increasing relationship between :code:`X` and :code:`Y`. The orange line represents the true mean of this data. Note the large amount of noise present.

.. image:: |filename|blog_media/2020/isotonic_python_package/relationship_zoomin.png

There is a classical algorithm for solving this problem nonparametrically, specifically `Isotonic regression <https://en.wikipedia.org/wiki/Isotonic_regression>`_. This simple algorithm is also implemented in `sklearn.isotonic <https://scikit-learn.org/stable/modules/generated/sklearn.isotonic.IsotonicRegression.html>`_. The classic algorithm is based on a piecewise constant approximation - with nodes at every data point - as well as minimizing (possibly weighted) `l^2` error.

The standard isotonic package works reasonably well, but there are a number of things I don't like about it. My data is often noisy with fatter than normal tails, which means that minimizing `l^2` error overweights outliers. Additionally, at the endpoints, sklearn's isotonic regression tends to be quite noisy.

The curves output by sklearn's isotonic model are piecewise constant with a large number of discontinuities (`O(N)` of them).

The size of the isotonic model can be very large - `O(N)`, in fact (with `N` the size of the training data). This is because in principle, the classical version isotonic regression allows every single value of :code:`x` to be a node.

The `isotonic` package I've written provides some modest improvements on this. It uses piecewise linear curves with a bounded (controllable) number of nodes - in this example, 30:

.. image:: |filename|blog_media/2020/isotonic_python_package/package_outputs.png

It also allows for non-:code:`l^2` penalties in order to handle noise better.

Isotonic regression for binary data
===================================

Another issue facing the standard isotonic regression model is binary data - where :code:`y in [0,1]`. Using RMS on binary data sometimes works (when there's lots of data and it's mean is far from :code:`0` and :code:`1`), but it's far from optimal.

For this reason I wrote a class :code:`isotonic.BinomialIsotonicRegression` which handles isotonic regression for the case of a binomial loss function.

.. image:: |filename|blog_media/2020/isotonic_python_package/binomial_isotonic.png

As is apparent from the figure, this generates more plausible results for binary isotonic regression (in a case with relatively few samples) than the standard sklearn package. The result is most pronounced at the endpoints where data is scarcest.

Code is available
=================

You can find the `code on my github <https://github.com/stucchio/isotonic>`_. It's pretty alpha at this time, so don't expect it to be perfect. Nevertheless, I'm currently using it in production code, in particular a trading strategy where the noise sensitivity of :code:`sklearn.isotonic.IsotonicRegression` was causing me problems. So while I don't guarantee it as being fit for any particular purpose, I'm gambling `:code:O($25,000)` on it every week or two.


Appendix: Mathematical Details
==============================

This appendix explains the mathematical details of the methods, as well as technical details of the parameterization. It is mainly intended to be used as a reference when understanding the code.

The package uses maximum likelihood for curve estimation, and uses the `Conjugate Gradient <https://en.wikipedia.org/wiki/Conjugate_gradient_method>`_ method (as implemented in :code:`scipy.optimize.minimize`) to actually compute this maximum.

Parameterizing the isotonic curves
----------------------------------

The first part of this is parameterizing the curves. The curves are parameterized by a set of :math:`\vec{x}_i, i=0 \ldots N-1` and a corresponding set of :math:`\vec{y}_i`, with :math:`\vec{y}_i \leq \vec{y}_{i+1}` for all :math:`i`. (I'm using zero-indexing to match the code.)

Since conjugate gradient doesn't deal with constraints, we must come up with a parameterization :math:`\alpha: \mathbb{R}^M \rightarrow \mathbb{R}^N` where the domain is unconstrained and the range satisfies the monotonicity constraint.

There are two cases to consider.

Real valued curves
~~~~~~~~~~~~~~~~~~

For real-valued isotonic regression, there are no constraints on :math:`\vec{y}_i` beyond the monotonicity constraint. Thus, we can use the parameterization:

.. math::
   \vec{y}_i = \vec{\alpha}_0 + \sum_{j=1}^i e^{\alpha_j}

Since :math:`\vec{y}_{i+1} - \vec{y}_{i} = e^{\alpha_{i+1}} > 0`, this trivially satisfies the monotonicity constraint.

In this case, the Jacobian can be computed to be:

.. math::
   \frac{\partial y_i}{\partial \alpha_0} = 1

.. math::
   \frac{\partial y_i}{\partial \alpha_j} = 1(j \leq i) e^{\alpha_j}, j \geq 1

Here the function :math:`1(x)` is equal to :math:`1` if it's argument is true and :math:`0` otherwise.

This parameterization is implemented `here <https://github.com/stucchio/isotonic/blob/master/isotonic/_base.py#L158>`_.

Probabilistic curves
~~~~~~~~~~~~~~~~~~~~

In the case of binomial isotonic regression, we have the additional constraint that :math:`0 < \vec{y}_{0}` and :math:`\vec{y}_{N-1} < 1` (since the curve represents a probability). We can parameterize this via:

.. math::
   \vec{y}_i = \frac{ \sum_{j=0}^i e^{\vec{\alpha}_{j}} }{ \sum_{j=0}^{N} e^{\vec{\alpha}_{j} } }


It is trivially easy to verify that this satisfies both the monotonicity constraint as well as the constraint that :math:`0 < \vec{y}_i < 1`. Note that in this case, there are :math:`N+1` parameters for an :math:`N` -dimensional vector :math:`\vec{y}`.

The Jacobian can be calculated to be:

.. math::
   \frac{\partial y_i}{\partial \alpha_j} = \frac{e^{\alpha_j} \left(1(j \leq i) \sum_{k=0}^{N+1} e^{\alpha_k} - \sum_{k=0}^i e^{\alpha_k} \right) }{ \left(\sum_{k=0}^N e^{\alpha_k} \right)^2 }

This parameterization is `implemented here <https://github.com/stucchio/isotonic/blob/master/isotonic/_base.py#L99>`_.

Different parameterizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

One parameterization for :math:`c(z; \vec{x}, \vec{y})` is piecewise constant, i.e.:

.. math::
   c(z; \vec{x}, \vec{y}) = \vec{y}_j

.. math::
   j(z) =  \textrm{arg max} \left\{ i | \vec{x}_i \leq z \right\}

In this case, simple calculus shows that

.. math::
   \frac{\partial}{ \partial y_k } c( z ; \vec{x}, \vec{y}) = \delta_{k,j(z)}

with :math:`j` as above.

This is implemented as the `PiecewiseConstantIsotonicCurve <https://github.com/stucchio/isotonic/blob/master/isotonic/curves.py#L41>`_ in the library.

Another parameterization is piecewise linear:

.. math::
   c(z; \vec{x}, \vec{y}) = (1-\beta) \vec{y}_{j(z)} + \beta \vec{y}_{j(z)+1}

.. math::
   \beta = \frac{z - \vec{x}_{j}}{\vec{x}_{j(z)+1} - \vec{x}_{j(z)}}

This has derivative:

.. math::
   \frac{\partial}{ \partial y_k } c( z ; \vec{x}, \vec{y}) = \beta \delta_{k,j+1} + (1-\beta)\delta_{k,j}

This is implemented as the `PiecewiseLinearIsotonicCurve  <https://github.com/stucchio/isotonic/blob/master/isotonic/curves.py#L60>`_.

Objective functions
-------------------

Some notation first. Let us consider a data set :math:`\vec{X}, \vec{Y}`. We will define a curve :math:`c(z;\vec{x}, \vec{y})`, taking values :math:`\vec{y}_i` at the points :math:`\vec{x}_i`, i.e. :math:`c(z=\vec{x}_i; \vec{x}, \vec{y}) = \vec{y}_i` and being parametrically related to :math:`\vec{x}, \vec{y}` elsewhere. Current implementations include piecewise linear and piecewise constant.

Supposing now that the nodes :math:`\vec{x}_i` are given, it remains to find the values :math:`\vec{y}` that minimize a loss function.

Real valued data
~~~~~~~~~~~~~~~~

In this case, our goal is to minimize the :math:`l^p` error:

.. math::
   \sum_{k} \left| \vec{Y}_k - c(\vec{X}_k ; \vec{x}, \vec{y}) \right|^p

Note that this corresponds to maximum likelihood under the model:

.. math::
   \vec{Y}_k = c(\vec{X}_k ; \vec{x}, \vec{y}) + \epsilon_k

with :math:`\epsilon_k` drawn from the distribution having pdf :math:`C e^{|Z|^p} dZ`.

Computing the gradient w.r.t. :math:`\vec{y}` yields:

.. math::
   \nabla_{\vec{y}} \sum_{k} \left| \vec{Y}_k - c(\vec{X}_k ; \vec{x}, \vec{y}) \right|^p = \sum_{k} p \left| \vec{Y}_k - c(\vec{X}_k ; \vec{x}, \vec{y}) \right|^{p-1} \nabla_y c(\vec{X}_k ;\vec{x}, \vec{y})

This is implemented in the library as `LpIsotonicRegression <https://github.com/stucchio/isotonic/blob/master/isotonic/lp_isotonic_regression.py#L11>`_.

Binomial data
~~~~~~~~~~~~~

Then given the data set, we can do max likelihood:

.. math::
   P(\vec{X}, \vec{Y} | c(z ; \vec{x}, \vec{y}) ) = \left[ \prod_{k|\vec{Y}_k = 1} c(z ; \vec{x}, \vec{y}) \right] \left[ \prod_{k|\vec{Y}_k = 0} (1 - c(z ; \vec{x}, \vec{y})) \right]

Taking logs and computing the gradient yields:

.. math::
   \nabla_y \ln P(\vec{X}, \vec{Y} | c(z ; \vec{x}, \vec{y}) ) = \left[ \sum_{k|\vec{Y}_k = 1} \frac{\nabla_y c(\vec{X}_k ;\vec{x}, \vec{y})}{ c(\vec{X}_k ; \vec{x}, \vec{y}) } - \sum_{k|\vec{Y}_k = 0} \frac{\nabla_y c(\vec{X}_k ;\vec{x}, \vec{y})}{1 - c( \vec{X}_k ; \vec{x}, \vec{y})}  \right]


Combining this with :math:`\nabla_\alpha \vec{y}` computed above, we can now compute :math:`\nabla_\alpha P(\vec{X}, \vec{Y} | c(z ; \vec{x}, \vec{y}) )`. This is sufficient to run conjugate gradient and other optimization algorithms.

This is implemented in the library as `BinomialIsotonicRegression <https://github.com/stucchio/isotonic/blob/master/isotonic/binomial_isotonic_regression.py#L11>`_.

Putting it all together
-----------------------

Choosing the nodes
~~~~~~~~~~~~~~~~~~

All the pieces are put together in a pretty straightforward way. For an :code:`M` - point interpolation, first the x-node points are chosen by finding the :code:`(2i+1)/2M` -th percentiles of the data, for :code:`i=0..M-1`.

We do this for the following reason. Consider standard isotonic regression where every single point is a node. Suppose that the value :math:`\vec{y}_0` is an outlier, and is dramatically smaller than would be expected. Then for all :math:`z < \vec{x}_0`, the isotonic estimator will be :math:`\vec{y}_0`. This is the characteristic of a very unstable estimator, and in my use cases this poses a significant problem.

In contrast, with the :code:`M` - point interpolation I'm using, the value of the isotonic estimator will be approximately :math:`\frac{1}{N_q} \sum_{i | \vec{x}_i < q} \vec{y}_{i}` where :math:`q` is the :math:`1/2M` -th quantile of the x-values and :math:`N_q` is the number of points with :math:`x_i < q`. This is a considerably more stable estimator.

Estimating the curve
~~~~~~~~~~~~~~~~~~~~

Once the nodes are given, estimation of the curve is pretty straightforward. We parameterize the curve as described above and use the conjugate gradient method to minimize the error. This can be generally expected to converge, due to the convexity of the error w.r.t. the curve. I have not encountered any cases where it doesn't.

(In the binomial case, convexity is technically broken due to the normalization.)

That's basically all there is to this.
