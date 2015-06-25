title: One tailed vs two tailed A/B tests - your decision procedure is the deciding factor
date: 2015-01-20 09:30
author: Chris Stucchio
tags: ab testing, decision rules

Over the past year or so, there have been a number of articles discussing the use of one tailed vs two tailed A/B tests. For example, [How Optimizely (Almost) Got Me Fired](http://blog.sumall.com/journal/optimizely-got-me-fired.html). The use of a one or two tailed test is an important issue. What [every](https://community.optimizely.com/t5/Strategy-Culture/Let-s-talk-about-Single-Tailed-vs-Double-Tailed/td-p/4220) [analysis](http://www.measuringu.com/blog/ab-testing.php) I've read fails to understand is that the issue cannot be decided at the level of statistics alone - it needs to be decided from within the context of a **decision procedure**.

When running an A/B test, the goal almost always to increase conversions rather than simply answer idle curiosity. To decide whether one tailed or two tailed is right for you, you need to understand your entire decision procedure rather than simply the statistics.

# What information do one and two tailed tests give you?

The rest of this post will be based on the frequentist paradigm. Most of the questions here vanish in the case of the Bayesian paradigm. Further, most people in the world are doing frequentist tests (e.g., anyone using VWO or Optimizely), so I'm going to stick to that paradigm.

In frequentist tests, you have a **null hypothesis**. The null hypothesis is what you believe to be true absent evidence to the contrary. Now suppose you've run a test and received a p-value. The p-value represents the probability of seeing a result at least that "extreme" in the event the null hypothesis were true. The lower the p-value, the less plausible it is that the null hypothesis is true.

Now suppose you are A/B testing a control and a variation, and you want to measure the difference in conversion rate between both variants.

The two tailed test takes as a a null hypothesis the belief that *both variations have equal conversion rates*.

The one tailed test takes as a null hypothesis the belief that the *variation is not better than the control, but could be worse*.

So the two tailed test might give you evidence that the control and variation are *different*, while the one tailed test gives evidence that the variation is *better* than the control.

# Decision procedures: finding the best out of a set of variations

Suppose we are deploying a brand new site. Two designers have gotten into a fight about which design the homepage should take, and an A/B test is needed to determine the best one. In this situation, there is no "default" choice.

To avoid biasing the decision process toward one variation or the other, a two tailed test should be used. The two tailed test looks for any evidence that one variation differs from the other - positive or negative. If variation 2 is better than variation 1 by a large margin, this information will be reported. If the reverse holds, it will still be reported.

So when your decision procedure has no default winner, a two tailed test is the most appropriate one to use.

# Deciding if an incremental improvement works

Consider a different situation. We've got a successful homepage already deployed. We've got a proposed change to the homepage which *might* help things. Should we deploy it?

In this case, absent strong evidence that the variation is better, we'll probably just stick with the existing page. Why mess with something that works?

For this situation, a one tailed test works just fine. The one tailed test will either give you evidence that the variant is significantly better than the control, or else it will not. In the latter event, you should conclude that the variant is probably not better than the control and might be worse.

Note that in the frequentist paradigm, it doesn't make sense to ask whether you have evidence that the variation is worse. You've already had a 5% chance of false positive in one tail of the test, so running a test on the other tail will increase your chance of false positive. But that's fine - this is information that won't change your decision.

# To sum it up

If your decision procedure looks like this:

1. Cook up a set of alternatives, all of which are on equal footing.
2. Run a test, figure out which is best.
3. Deploy the best. If no significant difference, choose one at random or by personal preference.

Then you should use a two tailed test.

If your decision procedure looks like this:

1. Choose a control, which is on superior footing to the alternatives.
2. Run a test, figure out if any alternative is better.
3. Deploy the alternative only if it's significantly better than the control.

Then it's perfectly fine to use a one tailed test. You won't learn if the alternative is worse or merely the same, but either way you'd have done the same thing and not deployed it.

Note that Andrew Gelman [also has a useful post on this topic](http://andrewgelman.com/2014/04/18/one-tailed-two-tailed/).
