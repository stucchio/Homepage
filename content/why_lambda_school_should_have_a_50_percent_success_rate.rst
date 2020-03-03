Cost Matters: Why Lambda School should have a lower success rate than college
#############################################################################
:date: 2020-03-03 08:30
:author: Chris Stucchio
:tags: education, decision theory


Lambda school has recently come under fire by the mainstream media for having success rates smaller than 100%, as well as for having a founder who is a nerd. The articles imply

(I'm not actually joking about that last part - the `MSM article <http://archive.is/HU2vj>`_ that I found literally talks about how he doesn't have enough friends.) But this critique is the height of innumeracy; there is no intrinsic reason Lambda School or any other institution *should* have high success rates.

In this blog post I'm going to do some really simple probability and expose an important tradeoff that I've observed people ignoring in many different contexts - Lambda School and MOOCs, in business, and elsewhere. This article is more about decision theory than Lambda School - but the recent controversy over Lambda School having a lower than 100% success rate makes a good jumping off point.

Lets do the math.


The basic math of a single gamble
=================================

Suppose we have the opportunity to make a gamble. If we make the gamble, we have a probability ``p`` of winning. If we win the gamble we earn a payoff of ``w``, whereas if we lose we earn a payoff of ``l``.

For example, the gamble might be "attend Lambda School", "go to college" or "buy clicks via google adwords which may or may not buy a product from our landing page". The payoff of a win (``w``) would be a higher paying job or a sale on a website. The loss of losing (``l``) would be the time and money spent on tuition or the money paid to Google for the click.

It's very easy to compute the expected value of this gamble is::

  E[gamble] = p*w + (1-p)*l

Assuming no risk aversion - fairly typical when ``w`` and ``l`` are not that large - we should take this gamble whenever ``E[gamble] > 0``. Doing some simple arithmetic, we discover that this gamble is positive sum whenever::

  w/l > (1-p)/p

(If this is a repeated game we should use the `Kelly Criterion <https://en.wikipedia.org/wiki/Kelly_criterion>`_ or some similar rule. I'm going to focus on the non-repeated case in this post.)

Another useful rearrangement is we break even when ``p = l/(w+l)``.

Sounds simple, right?

It's important to note that there are 3 different ways we can alter the parameters to make a gamble worthwhile:

- Increase ``w`` - make the payoff more attractive.
- Increase ``p`` - make a winning bet more likely.
- Decrease ``l`` - make the cost of losing lower.

The latter case is actually pretty important; consider the limiting case of ``l == 0``. In this case, there is a finite probability ``p`` of winning something, and even if you don't win you lose nothing. That's a good bet to take regardless of how low ``p`` is!

So far, nothing groundbreaking, right?

Concrete examples: Lambda School and Rutgers University
-------------------------------------------------------

Lets now consider Lambda School and cook up an oversimplified example.

I'll assume the applicant currently earns $30k/year. I'll assume that *if* the student is successful via Lambda School, their salary will increase to $70k/year. Furthermore, I'll assume the value of their time (before graduation) is $30k/year. I'll also use a 5 year time horizon.

Lambda School is a 9 month program. Valuing time at $30k/year, this means the cost of an unsuccessful attempt at Lambda School is ``l = $22.5k``.

If Lambda School succeeds, the winning payoff is a job earning $70k/year. The student will have to pay Lambda School 17% of this for 2 years (yielding a net pay of $58.1k/year) and after this they earn the full $70k. The excess over their original pay is then $28.1k for 2 years and $40k for 3 years - in total, ``w = $178k``.

On net, ``w/l = 7.91`` implying that even if the probability of success is only 15%, this is a reasonably good deal for the student.

Now lets examine Rutgers. I'm choosing Rutgers because it's my alma mater. Following the numbers `from this tweet thread <https://twitter.com/stucchio/status/1230510530973978627>`_, we learn the cost of Rutgers (a 4 year program) is $22.5k x 4 = $90k in lost income. Additionally tuition is $12k in state (assume a generous $6k after financial aid) adding another $24k for a total of $114k. This is paid whether the gamble pays off or not.

This means that ``w = 5 * $40k - 114k = $86k`` and ``l = $114k``. This yields ``w/l=0.75``, implying that even at 50% success probability, going to Rutgers is a bad deal for the student! Rutgers needs approximately a 60% success probability for the student to break even.

(Note: The actual success rate of Rutgers, `measured according to the criteria of Lambda School <https://twitter.com/stucchio/status/1230510532051947520>`_, is about 30%.)

You can play with these numbers a lot - take a 10 year time horizon, play with outcomes beyond "fail - 30k, success - 70k", etc.

But it's really hard to escape from the extreme cost advantage that ISAs provide: Lambda School doesn't cost very much for people who don't succeed. There's a reason that `Austen Allred <https://twitter.com/Austen>`_ constantly talks about alignment of incentives!


The basic math of a sorting rule
================================

Lets suppose now that we have multiple gambles we can choose to enter or not - say ``N` gambles, with ``i <- 1..N`` representing a particular gamble. Moreover, for each gamble, we know the success probability ``p[i]`` of that particular gamble.

For example, we might be choosing which students to admit to Lambda School or Rutgers.

As another example, we might be choosing which adwords (and landing pages matched to the adwords) we wish to bid on for CPC.

We are now faced with the task of choosing which gambles we want to take. Armed with the decision rule we came up with above we have a simple way to decide this: if ``w/l > (1-p[i])/p[i]`` we will accept gamble ``i``.


Lowering the cost of failure *should* lower your success rate
-------------------------------------------------------------

Let us now consider a set of gambles; lets assume that ``p[i] = i/10`` for ``i=0..10``. Suppose for simplicity that ``w=2, l=8``. This implies that the positive sum gambles are the ones with ``p[i] >= 0.8`` or ``i >= 8``.

If we choose gambles according to this rule, we will only choose to gamble at ``i=8,9,10``; the overall success probability is ``0.9``. This set of gambles should be thought of as a regular university; the cost of failure is high.

Suppose now we reduced the cost of failure; say instead of ``l=8`` we had ``l=2``. In this case, the positive sum gambles are the ones with ``p[i] >= 0.5`` or ``i=5...10``. The average success rate of over all of these gambles is ``0.75``, which is lower than the ``0.9`` we had at a cost of ``l=8``.

Here's the core economics of this. If you lower the cost of something, it makes sense to lower quality versions of that something.

Intuitive example: Wikipedia, Lambda School vs College
------------------------------------------------------

On the topic of educational institutions, consider my favorites: Wikipedia and Duckduckgo. These institutions have very high failure rates for me; quite often, I search for something and do not find what I'm looking for. Obviously, Wikipedia is not a failure simply because I search for lots of things I don't find.

And the reason for this is obvious; Wikipedia is free. If it's useful 20% of the time and takes me 5 seconds to search for something, that's an average of 25 seconds of search per useful result. That's a win.

In contrast, a college with a 20-30% success rate (and `they do exist <https://moneyinc.com/worst-colleges-in-america/>`_) is taking tens of thousands of dollars from students and providing very little value in return. This is much worse.

Lambda school operates somewhere in between these two extremes. It's a lot cheaper than college - particular for the people who don't succeed. This means that the socially optimal result (from the perspective of a student) is that Lambda School should admit more students until it's success rate drops significantly below college.

I understand the sentiment that high failure rates


You can never raise your conversion rate
========================================

Here's an example that someone at a major travel website told me about. The customer acquisition funnel consists of paying Google for adwords on a cost-per-click basis. Once people reach the site, a certain fraction of them make a purchase.

Suppose we have several different ad channels, i.e. keywords that can be bid on. When a customer converts the profit is $50.

The channels available are:
- A, with a CPC of $2 and a conversion rate of 10%. The cost per conversion here is $2/0.1 = $20, meaning the profit is $30 for people coming from this channel.
- B, with a CPC of $1 and a conversion rate of 3%. The cost per conversion here is $33, meaning the profit is $16 for people coming from this channel.
- C, with a CPC of $1 and a conversion rate of 1.5%. The cost per conversion here is $66, making this channel money losing.

Assuming these channels provide equal traffic, bids will be placed on channels A and B only. C is unprofitable so no bids are placed.

Now suppose the price of adwords falls by 30%; channel A now costs $1.4/click while B and C cost $0.7/click. At this point the cost per conversion of channel C has dropped to ``$0.7/0.015 = $46.67 < $50``. This channel then gets switched on.

However, the net result of this is that the conversion rate has dropped from ``(10% + 3%)/2=6.5%`` to ``(10%+3%+1.5%)/3 = 4.8%``. Profit margins have dropped too. The net result here is that traffic has increased by 50%, but the new 50% are low margin, barely profitable users with low conversion rates. These new users drag the average down.

On the flip side of this phenomenon, it's very difficult to *raise* conversion rates. Imagine a sitewide improvement that results in the conversion rate on every channel increasing by 40% (but prices remained the same). This raises the conversion rate of channel C to 2.1%, lowering the cost per conversion to $47.61 and making it profitable.

The average conversion rate goes to ``(14%+4.2%+2.1%)/3 = 6.76%``, a mere 4% improvement over the old conversion rate of ``(10%+3%)/2=6.5%``. If Channel C were twice the size of channel A, then the conversion rate would actually go down to ``(14%+4.2%+2x2.1%)/4 = 5.6%``!

On the other hand it's important to look at aggregate numbers. In these scenarios, improving conversion rates has increased sales by 50-100%. The additional sales have significantly lower margin, but it's still an increase in profits.


Why Indian software developers are lower quality than Western ones
==================================================================

I've made this argument `elsewhere in more detail <https://www.chrisstucchio.com/blog/2017/cobbs_douglas.html>`_, but I'll give a short summary here.

The cost of an American developer is approximately 3-10x the cost of a similar Indian developer. In my experience (I lived in India for many years), there are plenty of Indian developers and data scientists just as good as any in the US. (If you are seeking employees, I know of a good company that everyone is leaving from. I can connect you to people.)

Yet the reputation of Indian developers among Americans is quite low. People commonly talk about outsourced projects run by teams of idiots, and have generally strong criticisms of Indian developers in general.

I never had this experience, but I also subject anyone I hire in India to the same level of hiring rigor that I subject Americans to.

We can reconcile these two views simply by observing that as you lower the cost of a failure (e.g. making a bad hire), it is economically optimal to allow a higher rate of failure. This means that Indian companies competing with American companies should have a lower hiring bar, by the same logic as above. This will drag the *average* quality of Indian developers down; similarly low quality American developers would simply not get hired as developers.

Thus, the Indian software engineering market has lower quality simply because low costs have allowed a larger pool of people to enter.


Conclusion
==========

The interplay between individual success probabilities, cost of failure, and aggregate success probabilities is complex. It is simply innumerate to say, as `Austin Allred did <https://twitter.com/Austen/status/1231972469495324672>`_, that *"We will never be ok with 50% [success rate]."* As the cost of failure drops, as it does with Lambda School, the socially optimal success rate also drops.

(To be clear, I believe `@austen <https://twitter.com/Austen>`_ probably knows this and is merely attempting to placate innumerate journalists.)

Simple economics tells us that the lower the cost of failure, the more failed attempts should be made. When the cost of failure goes down, any critique of reduced success rates is hopelessly innumerate.
