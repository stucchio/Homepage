Scalably Detecting Odd-looking Histograms
#########################################
:date: 2020-03-24 08:30
:author: Chris Stucchio
:tags: python, statistics, outlier detection

A lot of suspicious behavior can be detected simply by looking at a histogram. Here's a nice example. There's a paper `Distributions of p-values smaller than .05 in Psychology: What is going on? <|filename|blog_media/2020/detecting_funny_histograms/bbbec3c0722a5f0eedd09f5f23043a47b6a6.pdf>`_ which attempts to characterize the level of data manipulation performed in academic psychology. Now under normal circumstances, one would expect a nice smooth distribution of p-values resulting from honest statistical analysis.

What actually shows up when they measure it is something else entirely:

.. image:: |filename|blog_media/2020/detecting_funny_histograms/p_values.png

Another example happened to me when I was doing credit underwriting. A front-line team came to me with concerns that some of our customers might not be genuine, and in fact some of them might be committing fraud! Curious, I started digging into the data and made a histogram to get an idea of spending per customer. The graph looked something like this:

.. image:: |filename|blog_media/2020/detecting_funny_histograms/example_odd_histogram.png

The value :code:`x=10` corresponded to the credit limit we were giving out to many of our customers. For some reason, a certain cohort of users were spending as much as possible on the credit lines we gave them. Further investigation determined that most of those customers were not repaying the money we lent them.

In contrast, under normal circumstances, a graph of the same quantity would typically kook like this:

.. image:: |filename|blog_media/2020/detecting_funny_histograms/business_as_usual.png

A third example - with graphs very similar to the previous example - happened to me when debugging some DB performance issues. We had a database in US-East which was replicated to US-West. Read performance in US-West was weirdly slow, and when we made a histogram of request times, it turned out that the slowness was driven primarily by a spike at around 90ms. Coincidentally, 90ms was the ping time between our US-East and US-West servers. It turned out that a misconfiguration resulted in the US-West servers occasionally querying the US-East read replica instead of the US-West one, adding 90ms to the latency.

A fourth example comes from the paper `Under Pressure?  Performance Evaluation of Police Officers as an Incentive to Cheat: Evidence from Drug Crimes in Russia <|filename|blog_media/2020/detecting_funny_histograms/EEAESEM2019-1123.pdf>`_ which discovers odd spikes in the amount of drugs found in police searches.

.. image:: |filename|blog_media/2020/detecting_funny_histograms/drugs.png

It sure is very strange that so many criminals all choose to carry the exact amount of heroin needed to trigger harsher sentencing thresholds, and never a few grams less.

In short, many histograms should be relatively smooth and decreasing. When such histograms display a spike, that spike is a warning sign that something is wrong and we should give it further attention.

In all the cases above, I made these histograms as part of a post-hoc analysis. Once the existence of a problem was suspected, further evidence was gathered and the spike in the histogram was one piece of evidence. I've always been interested in the question - can we instead automatically scan histograms for spikes like the above and alert humans to a possible problem when they arise?

This blog post answers the question in the affirmative, at least theoretically.


Mathematically modeling a single test
=====================================

To model this problem in the frequentist hypothesis testing framework, let us assume we have a continuous probability distributions :math:`f` which is supported on :math:`[0,\infty)`. As our null hypothesis - i.e. nothing unusual to report - we'll assume this distribution is absolutely continuous with respect to Lebesgue measure and that it has pdf :math:`f(x) dx` which is monotonically decreasing, i.e. :math:`f(y) \leq f(x)` for :math:`y \geq x` (almost everywhere).

In contrast, for the alternative hypothesis - something worth flagging as potentially bad - I'll assume that the distribution is a mixture distribution with pdf :math:`(1-\beta) f(x) + \beta s(x) dx`. Here :math:`s(x)` is monotonically increasing, or more typically :math:`s(x) = \delta(x-x_0)`.

**Observation:** Consider a probability distribution :math:`f(x)` that is monotonically decreasing. Then the cumulative distribution function :math:`F(x)=\int_0^x f(t) dt` is `concave <https://en.wikipedia.org/wiki/Concave_function>`_. This can be proven by noting that it's derivative, :math:`F'(x) = f(x)` is monotonically decreasing.

Our hypothesis test for distinguishing between the null and alternative hypothesis will be based on concavity. Specifically, if there are spikes in a histogram of the pdf of a distribution, then it's CDF may cease to be concave at the point of the spike. Here's an illustration. First, consider the empirical CDF of a distribution which is monotonically decreasing:

.. image:: |filename|blog_media/2020/detecting_funny_histograms/concave_cdf.png

This graph is clearly concave. The red line illustrates a chord which must, by concavity, remain below the actual curve.

In contrast, a pdf with a spike in it will fail to be concave near the spike. Here's an illustration:

.. image:: |filename|blog_media/2020/detecting_funny_histograms/non_concave_cdf.png

At :math:`x=10` the chord (the red line) is above the graph of the CDF (the green line).

In mathematical terms, `concavity <https://en.wikipedia.org/wiki/Concave_function>`_ of the true CDF can be expressed as the relation:

.. math::
   F(x + \alpha (y-x)) \geq (1-\alpha)F(x) + \alpha F(y)

or equivalently:

.. math::
   F(x + \alpha (y-x)) - (1-\alpha)F(x) - \alpha F(y) \geq 0

Since we do not know :math:`F(x)` exactly, we of course cannot measure this directly. But given a sample, we can construct the empirical CDF which is nearly as good:

.. math::
   F_n(x) = \frac{1}{n} \sum_{i=1}^n 1_{x \geq x_i}.

Using the empirical CDF and the definition of concavity suggests a test statistic which we can use:

.. math::
   q = \min_{0 \leq \alpha \leq 1} \min_{x} \min_{y \geq x} \left[ F_n(x + \alpha (y-x)) - (1-\alpha)F_n(x) - \alpha F_n(y) \right]

Our goal is to show that if this test statistic is sufficiently negative, then a spike must exist.

When :math:`q` becomes negative, this shows that :math:`F_n(x)` is non-concave. However, the empirical distribution function is by definition non-concave, as can be seen clearly when we zoom in:

.. image:: |filename|blog_media/2020/detecting_funny_histograms/concave_zoomin.png

Mathematically we can also see this simply by noting that :math:`1_{x \geq x_i}` is not concave. However, this non-concavity has order of magnitude :math:`O(n^{-1})`, so to deal with this we can simply demand that :math:`q < -1/n`.

There is a larger problem caused - potentially - by deviation between the empirical distribution :math:`F_n(x)` and the true, continuous and concave cdf :math:`F(x)`. This however can also be controlled and will be controlled in the next section.

Controlling false positives
---------------------------

To control false positives, there is a useful mathematical tool we can use to control this - the `DKW inequality <https://en.wikipedia.org/wiki/Dvoretzky%E2%80%93Kiefer%E2%80%93Wolfowitz_inequality>`_ (abbreviating Dvoretzky–Kiefer–Wolfowitz). This is  a stronger version of the `Glivenko-Cantelli Theorem <https://en.wikipedia.org/wiki/Glivenko%E2%80%93Cantelli_theorem>`_, but which provides uniform convergence over the range of the cdf.

We use it as follows.

Recall that :math:`q` is defind as a minima of :math:`\left[ F_n(x+\alpha(y-x)) - (1-\alpha)F_n(x) - \alpha F_n(y)\right]`. Let us choose :math:`(x,y,\alpha)` now to be the value at which that minima is achieved. Note that this requires that :math:`x < y` are two points in the domain of :math:`F(x)` and :math:`\alpha \in [0,1]`. Let us also define :math:`z=x + \alpha(y-x)` in order to simplify the calculation.

Now lets do some arithmetic, starting from the definition of concavity of the CDF:

.. math::
   F(z) - (1-\alpha)F(x) - \alpha F(y) =

.. math::
   = F(z) - (1-\alpha)F(x) - \alpha F(y) - q + q

.. math::
   = F(z) - (1-\alpha)F(x) -  \alpha F(y) - \left[ F_n(z) - (1-\alpha)F_n(x) - \alpha F_n(y)\right] + q

(This line follows since :math:`\left[ F_n(x+\alpha(y-x)) - (1-\alpha)F_n(x) - \alpha F_n(y)\right] = q` due to our choice of :math:`(x,y,\alpha)` above.)

.. math::
   = \left(F(z) - F_n(z) \right) + (1-\alpha) \left(F(x) - F_n(x) \right) + \alpha \left( F(y)-F_n(y) \right) + q

The DKW inequality tells us that for any :math:`\epsilon > 0`,

.. math::
   P\left[\sup_x (F_n(x) - F(x)) > \epsilon \right] \leq e^{-2n\epsilon^2}

Substituting this into the above, we can therefore say that with probability :math:`e^{-2n\epsilon^2}`,

.. math::
   F(z) - (1-\alpha)F(x) - \alpha F(y) \leq q + 2\epsilon

If :math:`q + 2\epsilon < 0`, this lets us reject the null hypothesis that :math:`F(x)` is concave, or equivalently, that :math:`f(x)` is monotonically decreasing. Conversely, given a value of :math:`q`, we can invert to gain a p-value. We summarize this as a theorem:

**Theorem 1:** Assume the null hypothesis of concavity is true. Let :math:`q` be defined as above. Then if :math:`q < 0`, we can reject the null hypothesis (that :math:`f(x)` is decreasing monotonically) with p-value :math:`p=e^{-n q^2/2}`.

This convergence is exponential but at a slow rate. Much like a `Kolmogorov-Smirnov <https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test>`_, the statistical power is relatively low compared to parametric tests (such as `Anderson-Darling <https://en.wikipedia.org/wiki/Anderson%E2%80%93Darling_test>`_) that are not based on the `DKW inequality <https://en.wikipedia.org/wiki/Dvoretzky%E2%80%93Kiefer%E2%80%93Wolfowitz_inequality>`_.

Controlling true positives
--------------------------

Let us now examine the true positive rate and attempt to compute statistical power. As a simple alternative hypothesis, let us take a mixture model:

.. math::
   F(x) = (1-\beta) f(x) + \beta \delta(x-x_0)

Here :math:`f(x)` is monotone decreasing and :math:`\delta(x-x_0)` is the point mass at :math:`x_0`. Let us attempt to compute


.. math::
   \min_{0 \leq \alpha \leq 1} \min_{x} \min_{y \geq x} \left[ F(x + \alpha (y-x)) - (1-\alpha)F(x) - \alpha F(y) \right]

Let :math:`x=x_0-\epsilon`, :math:`y=x_0+\epsilon^2` and :math:`\alpha=\frac{1-\epsilon}{1+\epsilon}`. Then:

.. math::
   x + \alpha(y-x) = (x_0-\epsilon) + \frac{1-\epsilon}{1+\epsilon}\left[x_0+\epsilon^2 - (x_0-\epsilon)\right] = x_0-\frac{\epsilon^3}{1+\epsilon}

Now substituting this in, we discover:

.. math::
   F(x + \alpha (y-x)) - (1-\alpha)F(x) - \alpha F(y)

.. math::
   = F(x_0-\frac{\epsilon^3}{1+\epsilon}) - \frac{2\epsilon}{1+\epsilon} F(x_0-\epsilon) - \frac{1-\epsilon}{1+\epsilon} F(x_0+\epsilon)


Letting :math:`\bar{F}(x) = \int_0^x f(x) dx`, we observe that :math:`F(x) = (1-\beta)\bar{F}(x) + 1_{x \geq x_0}`. Since :math:`f(x)` is absolutely continuous, :math:`\bar{F}(x)` is of course a continuous function.

Let us now take the limit as :math:`\epsilon \rightarrow 0`:

.. math::
   \lim_{\epsilon \rightarrow 0} F(x_0-\frac{\epsilon^3}{1+\epsilon}) - \frac{2\epsilon}{1+\epsilon} F(x_0-\epsilon) - \frac{1-\epsilon}{1+\epsilon} F(x_0+\epsilon)

.. math::
   = (1-\beta)\bar{F}(x_0 - 0) - \frac{2\cdot0}{1+0} (1-\beta)\bar{F}(x_0 - 0) - \frac{1-0}{1+0} \left( (1-\beta) \bar{F}(x_0 + 0) + \beta \right)

.. math::
   = (1-\beta)\bar{F}(x_0) - 0 - (1-\beta) \bar{F}(x_0) - \beta

.. math::
   = -\beta


This implies that

.. math::
   \min_{0 \leq \alpha \leq 1} \min_{x} \min_{y \geq x} \left[ F(x + \alpha (y-x)) - (1-\alpha)F(x) - \alpha F(y) \right] \leq - \beta,

since the minima is of course smaller than any limit.

By the same argument as in the previous section - using the DKQ inequality to relate :math:`F(x)` to :math:`F_n(x)` - we can therefore conclude that:

.. math::
   q \leq - \beta + 2\epsilon

with probability :math:`1-e^{-2n\epsilon^2}`.

Distinguishing the null and alternative hypothesis
--------------------------------------------------

We can combine these results into a hypothesis test which is capable of distinguishing between the null and alternative hypothesis with any desired statistical power.

**Theorem 2:** Let :math:`p` be a specified p-value threshold and let :math:`r` be a desired statistical power. Let us reject the null hypothesis whenever

.. math::
   q \leq 2 \sqrt{\frac{\ln(p)}{2n}}.

Suppose now that

.. math::
   \beta \geq 2 \left(\sqrt{\frac{-\ln(p)}{2n}} + \sqrt{\frac{-\ln(1-r)}{2n}} \right).

Then with probability at least :math:`r`, we will reject the null hypothesis.

Example numbers and slow convergence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Due to the slowness of the convergence implied by the DKW inequality, we unfortunately need fairly large :math:`n` (or large :math:`\beta`) for this test to be useful.

+-------+---------------+
| n     | :math:`\beta` |
+=======+===============+
| 1000  | 0.155         |
+-------+---------------+
| 2000  | 0.109         |
+-------+---------------+
| 5000  | 0.0692        |
+-------+---------------+
| 10000 | 0.0490        |
+-------+---------------+
| 25000 | 0.0310        |
+-------+---------------+
| 100000| 0.0155        |
+-------+---------------+

Thus, this method is really only suitable for detecting either large anomalies or in situations with large sample sizes.

Somewhat importantly, this method is not particularly sensitive to the p-value cutoff. For example, with a 1% cutoff rather than a 5%, we can detect spikes of size :math:`\beta=0.055` at :math:`n=10000`.

This makes the method reasonably suitable for surveillance purposes. By setting the p-value cutoff reasonably low (e.g. 1% or 0.1%), we sacrifice very little measurement power on a per-test basis. This allows us to run many versions of this test in parallel and then use either the `Sidak correction <https://en.wikipedia.org/wiki/%C5%A0id%C3%A1k_correction>`_ to control the group-wise false positive rate or `Benjamini-Hochburg <https://en.wikipedia.org/wiki/False_discovery_rate#Benjamini%E2%80%93Hochberg_procedure>`_ to control the false discovery rate.

Conclusion
==========

At the moment this test is not all I was hoping for. It's quite versatile, in the sense of being fully nonparametric and assuming little beyond the underlying distribution being monotone decreasing. But while theoretically the convergence is what one would expect, in practice the constants involved are large. I can only detect spikes in histograms after they've become significantly larger than I'd otherwise like.

However, it's still certainly better than nothing. This method would have worked in several of the practical examples I described at the beginning and would have flagged issues earlier than than I detected them via manual processes. I do believe this method is worth adding to suites of automated anomaly detection. But if anyone can think of ways to improve this method, I'd love to hear about them.

I've searched, but haven't found a lot of papers on this. One of the closest related ones is `Multiscale Testing of Qualitative Hypotheses <|filename|blog_media/2020/detecting_funny_histograms/euclid.aos.996986504.pdf>`_.
