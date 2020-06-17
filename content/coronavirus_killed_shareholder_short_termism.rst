Shareholder Short-Termism Theory has Died of COVID-19
#####################################################
:date: 2020-06-17 08:30
:author: Chris Stucchio
:tags: economics
:featured: true

It's become a popular meme that "shareholders only care about the next quarter". Lots of people make arguments like this - for example, `Jamie Dimon and Warren Buffet <https://www.wsj.com/articles/short-termism-is-harming-the-economy-1528336801>`_. As the meme goes, shareholders only care about the next quarter of earnings, and CEOs make decisions accordingly - sacrificing long term profitability to meet quarterly expectations.

But is this meme true?

Relatedly, consider

Coronavirus gives us a great empirical test of this theory.

Formalizing the theory
======================

The first step in answering this question is to formalize the theory. The most straightforward way I can think of to do this is through the lens of `net present value <https://www.investopedia.com/terms/n/npv.asp>`_, albeit with a modified discount rate.

This framework says that the value of any cash generating asset is given by:

.. math::
   V = \sum_{t=1}^\infty R_t d_t

In this sum, :math:`R_t` is the cash flow in time period :math:`t` and :math:`d_t` is the *discount factor* of time :math:`t`.

Here's a fairly simple example - a US treasury bill guaranteed to pay a $100 coupon for 3 periods and then to pay a final $10,000 in the 4'th. In tabular form:

========== =====
date       R
========== =====
2020-06-30 100
2020-09-30 100
2020-12-31 100
2021-03-31 10000
========== =====

To complete the calculation, we need to time discount each cash payment. This is typically done by taking the risk free interest rate - say 5% - and applying that to each time period. For example:


========== ===== ==== =======
date       R     d    R*d
========== ===== ==== =======
2020-06-30 100   1.00 100.00
2020-09-30 100   0.99 98.75
2020-12-31 100   0.98 97.51
2021-03-31 10000 0.96 9631.85
========== ===== ==== =======

Finally, the value of the bond is the sum of the :code:`R*d` column, which is $9928.12 in this example.

Short-Termism in this framework
-------------------------------

In this framework, short-termism can be straightforwardly represented by the :code:`d` column - specifically, :code:`d` will rapidly decrease over time. For instance, a very short term valuation of the same bond (a 25% discount rate) might be described as:

========== ===== ==== =======
date       R     d    R*d
========== ===== ==== =======
2020-06-30 100   1.00 100.00
2020-09-30 100   0.94 93.90
2020-12-31 100   0.88 88.17
2021-03-31 10000 0.83 8289.90
========== ===== ==== =======

which yields a valuation of $8571.97.

Given that Treasury valuations do not look anything like this, we can certainly see that *bond* investors are not vulnerable to the short-termism that *stock* investors purportedly suffer from.

The straw man version of "shareholders only care about the next quarter" would mean that :code:`d=0` for all quarters past the next one.

I will examine this model for mathematical understanding, though I don't think it's a particularly fair thing to do.

Modeling an uncertain future
----------------------------

Now let us consider a stock rather than a bond - specifically, a pharma company with a single drug in the final phase of clinical trials which end in 1 year.

The cashflow is quite certain for the next 1 year - :code:`R[0:4] == 0`, i.e. the company loses money to run the clinical trial and pays nothing to shareholders. After 1 year, there are two possible outcomes:

1. The good outcome. :code:`R_good = +1000`, the drug works, everyone buys it for 17 years, company is valuable.
2. The bad outcome. :code:`R_bad = 0`, the drug does not work, company is worthless.

==========      ======  =====           =======
date            R_good  R_bad           d
==========      ======  =====           =======
2020-06-30	0	0	        1.0000
2020-09-30	0	0	        0.9987
2020-12-31	0	0	        0.9975
2021-03-31	0	0	        0.9963
2021-06-30	1000	0	        0.9950
2021-09-30	1000	0	        0.9938
.               .       .               .
2036-06-30	1000	0	        0.9231
2036-09-30	1000	0	        0.9220
2036-12-31	1000	0	        0.9208
2037-03-31	1000	0	        0.9197
==========      ======  =====           =======

The company has two eventual valuations (at a long-termist 0.5% discount rate), depending on whether we believe the :code:`R_good` or :code:`R_bad` column represents the future - $61,238 in the first case and $0 in the second.

If we assume a 60% chance of the drug getting through clinical trials, then the value of the company would be :code:`0.6 * $61238 + 0.4 * 0 = 36742.90`.


Note that in the straw man case of *literally only the next quarter matters*, this company is worth $0 in all possible scenarios - it's first actual profit is 1 year out.

Long term investors *appear* short term
=======================================

Lets now consider a long term investor who is evaluating a blue chip, highly stable stock. This stock regularly has earnings of $100. Then one quarter, it misses earnings and only reports $75!

An investor infected by short-termism will significantly cut their evaluation of the company - since :code:`d=0` for all future periods, the value drops from $100 to $75, a 25% decrease.

Let us now consider a long term investor.

==========      ======         =======
date            R              d
==========      ======         =======
2020-06-30	75	       1.0000
2020-09-30	100	       0.9987
2020-12-31	100	       0.9975
2021-03-31	100	       0.9963
2021-06-30	100	       0.9950
.               .              .
==========      ======         =======

Over 18 years, the value of this revenue stream works out to be $6498. In contrast, had earnings for one quarter not been missed, it would be $6523, a difference of 0.4%. Thus, if there is a drop in share price of significantly more than 0.4%, one might hypothesize that this is due to the market taking a short termist view.

Let us now consider a long term investor who actively tries to think through cause and effect. Earnings decreased, and there must be some reason for it! The question to ask is therefore whether this reduction in a single quarter's earnings will continue into the future. We encounter a situation similar to the pharma stock discussed earlier:

==========      ======  =====           =======
date            R_good  R_bad           d
==========      ======  =====           =======
2020-06-30	75	75	        1.0000
2020-09-30	100	75	        0.9987
.               .       .               .
2036-09-30	100	75	        0.9220
2036-12-31	100	75	        0.9208
2037-03-31	100	75	        0.9197
==========      ======  =====           =======

In the :code:`R_bad` scenario, the company will only be worth $4892 (a 25% decrease from it's previous value).

If the long term investor believes that there is a 40% chance of this occurring, then the value of the stock decreases to $5855.75, a 10% drop!

Even though the long term investor doesn't care much about a single quarter's earnings, he cares a lot about whether this predicts many more quarters of reduced earnings. This means that even long term investors behave in the manner that others describe as "short-termist".

As a result, both the short-termism theory and the long-termism theory *make very similar predictions*. The fact that stock prices move significantly in response to missed earnings estimates is insufficient to distinguish between these two theories.


Coronavirus as a natural experiment
===================================

Coronavirus provides a great natural experiment to help disambiguate test this theory. A large number of stocks are going to have several quarters of significantly reduced earnings, but there is very little uncertainty as to the reason.

We know that right now people don't go to $SBUX, $MCD or $CMG. This will be a big hit to their earnings. But on the flip side we know exactly why - people haven't suddenly decided they dislike Big Macs, they just don't want to catch coronavirus.

Meanwhile, we're being treated to articles like `The Great Divide Between Stocks & The Economy <https://www.zerohedge.com/markets/great-divide-between-stocks-economy>`_ which discuss a significant deviation between stock market performance and *short term* economic indicators.

One thing is pretty clear: the next couple of quarters of earnings are going to suck. But unlike many earnings misses, we know exactly why. And for most blue chip stocks in the S&P 500, we have great reason to believe that this is strictly temporary, and once coronavirus is dealt with things will go back to normal.

.. figure:: |filename|blog_media/2020/coronavirus_killed_shareholder_short_termism/spy.png
   :figwidth: 460px

   SPY over time.

Although SPY is nowadays driven predominantly by technology companies, even brick and mortar companies that are likely to survive the crisis have a similar share price:
This is even true of solid brick and mortar companies such as McDonald's or Starbucks.

.. figure:: |filename|blog_media/2020/coronavirus_killed_shareholder_short_termism/mcd.png
   :figwidth: 460px

   MCD over time.

.. figure:: |filename|blog_media/2020/coronavirus_killed_shareholder_short_termism/sbux.png
   :figwidth: 460px

   SBUX over time.

If shareholders only care about the next quarter, there is no case to make that $SBUX is worth holding.

However, if shareholders are looking to the long term, then $SBUX and $MCD are pretty solid stocks to hold. If investors have a low discount rate, the impact of the next couple of quarters on LTV is not that big. As long as investors are convinced that there *actually is* a long term for the company, $SBUX and $MCD remain solid investments. The calculus of a long term investor is exactly as described before:

==========      ======            =======
date            R_SBUX            d
==========      ======            =======
2020-06-30	50                1.0000
2020-09-30	50	          0.9987
.               .                 .
2036-09-30	90	          0.9220
2036-12-31	90	          0.9208
2037-03-31	90	          0.9197
==========      ======            =======

They may not be quite as large after the crisis as before - some locations will certainly close - but overall the revenue stream is likely to continue.

In contrast, other stocks such as $CCL (Carnival Cruise Lines) do not have such a rosy outlook. Unlike $SBUX, $CCL may simply go bankrupt - in that case, shareholders get nothing.

.. figure:: |filename|blog_media/2020/coronavirus_killed_shareholder_short_termism/ccl.png
   :figwidth: 460px

   CCL over time.

$CCL is has a very uncertain future. It is likely that it's business will remain solid if it can survive through the crisis - it's August cruises are already fully booked. However, it is not clear that $CCL can actually survive the crisis without going through bankruptcy first. Ships are expensive to store and CCL has financing costs, and it's not clear it can do this without incoming revenue.

This makes it's valuation look a lot more uncertain, with both a good and bad outcome:

==========      ======  =====           =======
date            R_good  R_bad           d
==========      ======  =====           =======
2020-06-30	0	0	        1.0000
2020-09-30	0	0	        0.9987
.               .       .               .
2036-09-30	100	0	        0.9220
2036-12-31	100	0	        0.9208
2037-03-31	100	0	        0.9197
==========      ======  =====           =======

Thus, the stock price of $CCL is remaining low because it is unclear that it ever will come back. There is a high probability assigned to the bad outcome and thus the LTV is low.

These results are completely inconsistent with short-termism
------------------------------------------------------------

These results are completely inconsistent with a short term "only the next quarter matters" view of the market.

Consider a short term view of $CCL. In the short term view the only quarters which matter are the next few ones, and *these quarters are all zero* in both the good and bad scenarios. Thus, $CCL is completely worthless for anything besides option value in all possible worlds.

But *the same thing is also true for $SBUX and $MCD*. For an investor with only short term horizons, $SBUX and $MCD should also be worthless. Yet they have almost completely recovered in value, along with a wide variety of other companies that have a great long term value prop but a terrible short term.

All about liquidity injections
------------------------------

If I had a comment section, I would fully expect someone to talk about how this is all invalid because of the Fed.

.. figure:: |filename|blog_media/2020/coronavirus_killed_shareholder_short_termism/brrr.jpg
   :figwidth: 500px

But this betrays a fundamental misunderstanding of accounting. When "money printer go brrr", the actual mechanism by which this happens is that new debt is issued at favorable terms. Taking out a loan is not earnings so the short term forecast for a company impacted by Coronavirus is unchanged. A short term investor will be completely unmoved by this!

The money printer does have one very important effect - it increases the odds significantly that a company will survive the crisis and have a good *long term* returns. The next couple of quarters will suck, but the long term value of the company remains.

The Short-Termism theory has died of COVID
==========================================

Coronavirus is a great natural experiment for a lot of things.

One of the most important things we can take away from it is the conclusion that equity markets are fundamentally focused on the long term value of the companies being traded. There are fast responses to problems with next quarter earnings, but these are primarily driven by the fact that problems in the short run tend to be indicative of more fundamental issues.

Now that we have a systematic example where we know that short run problems are strictly short run, we can safely disambiguate between short termism and long termism. The result is very clear; the market is predominantly focused on the long term.


**Disclosure:** Long $SBUX, $CCL.
