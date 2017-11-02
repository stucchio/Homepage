Why Bangalore companies companies should be very different from San Fransisco ones - an application of Cobb-Douglas
###################################################################################################################
:date: 2017-10-31 01:30
:author: Chris Stucchio
:tags: economics, cobb douglas, business


Some time back, I was involved in a discussion with folks at an India-based software company. An important question was asked - why isn't this company as productive (defined as revenue/employee) as it's western competitors, and what can be done to change this situation? In this discussion, I put forward an unexpected thesis: if this company were profit maximizing, then it's productivity should *always* be far lower than any western company. During the ensuing conversation, I came to realize that very few people were aware of the `Cobb-Douglas model of productio <https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function>`_, on which I was basing my counterintuitive conclusions.

I've observed that the topic of Cobb-Douglas has come up quite a few times, and several folks have asked me to write up a description of it. Hence, this blog post. In my opinion, Cobb-Douglas is a very useful model to have in one's cognitive toolbox.

Setting up the problem
======================

To lay out the basics of the problem, consider two competing companies - Bangalore Pvt. Ltd. and Cupertino Inc. For concreteness, let us say that these two companies are both sotware companies catering to the global market and they are direct competitors.

The question now arises; how should Bangalore and Cupertino allocate their capital?

For a software company, there are two primary uses toward which capital can be directed:

- Marketing. Both Bangalore and Cupertino can direct an extra $1 of spending towards adwords, facebook ads, attendance at conferences, and similar things. Both companies will receive the same amount of *exposure* on their marginal dollar.
- Employees. Bangalore and Cupertino can both spend money on employees, but in this case they receive *different* returns on investment. In Bangalore, a typical employee might cost 100,000 rupees/month, whereas in Cupertino an employee might cost $100,000/year. This is approximately a 5x cost difference if we round up 1 lac rupees/month to $20,000/year.

Let us now model what the effect of each resource is on revenue.

It's a simple arithmetic identity is that revenue :math:`R` is equal to:

.. math::
    R = L \cdot M

The values

.. math::
   L = L(\textrm{features, marketing strategy, etc})

is the probability of any individual prospect making a purchase multiplied by the value of that purchase, and

.. math::
    M = M(\textrm{marketing spend})

is the number of prospects who can be reached by marketing as a function of money spent on it.

We choose this decomposition because it helps us understand the impact of two separate resources:

- The value :math:`L` is mainly increased by spending money on additional *labor*. Engineers can build features, which increase value for customers and allow the product to be sold for more money. Marketers may improve the brand value, increasing the probability of a sale.
- The value :math:`M` is increased by spending money on additional *marketing*. It's a simple machine - money is spent on facebook ads, conferences, TV commercials, and more people become exposed to the product.

Diminishing returns to labor
----------------------------

To understand the relationship between resources and production, let us take the following exercise. Suppose we have a large set of projects, each with a certain cost and benefit:

- Integrate the software with Salesforce, cost 100 hours, benefit $50/prospect.
- Come up with a more enterprisey-sounding brand, cost 40 hours, benefit $10/prospect.
- Slap some AI on top of the software, cost 2000 hours, benefit $60/prospect.
- etc...

Fundamentally, I'm making two important assumptions here:

1. The projects have no interdependencies.
2. The amount of labor required for each project is small compared to the overall amount of labor.

Let us assume the corporate strategy is to spend whatever amount of labor we have on this collection of projects in order of decreasing ROI. This means that if we sort the list of projects by ROI = benefit / cost, then the corporate strategy will be to take on the highest ROI projects first.

Here's a typical result:

.. image:: |filename|blog_media/2017/cobbs_douglas/diminishing_returns.png

Note that the `xkcd` plotting style is used `to illustrate this is a schematic drawing <https://www.chrisstucchio.com/blog/2014/why_xkcd_style_graphs_are_important.html>`_, and should not be taken too literally.

The graph was made as follows:

.. code:: python

    data = pandas.DataFrame({ 'cost' : uniform(10,100).rvs(50), 'benefit' : uniform(1,100).rvs(50) })
    data['roi'] = data['benefit'] / data['cost']
    data = data.sort_values(['roi'], ascending=False)

    step(cumsum(data['cost']), cumsum(data['benefit'])) #Like `plot(...)`, except that it shows steps at each data point.

As noted above, the units on the y-axis are dollars per prospect.

Diminishing returns on marketing
--------------------------------


The `Cobb-Douglas <https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function>`_ model is an economic model useful for describing the effects of complementary factors of production.
