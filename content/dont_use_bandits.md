title: Don't use Bandit Algorithms - they probably won't work for you
date: 2015-01-27 09:00
author: Chris Stucchio
tags: statistics, bandit algorithms, ab testing
nolinkback: true
category: statistics

Several years back, I wrote an article [advocating in favor of using bandit algorithms](/blog/2012/bandit_algorithms_vs_ab.html). In retrospect, the article I wrote was incorrect, and I should have phrased it differently. I made no mathematical mistakes in the article. Every fact I said is true. But the implications of this article and the way it has been interpreted by others is deeply wrong, and I'm going to take the opportunity now to correct what I said.

Before I get into the details, I want to make a particular point very clear. **If you don't understand all the math in this post**, don't use bandit algorithms at all. Just use ordinary A/B tests to make product decisions. Go use optimizely or visual website optimizer to set up and deliver your A/B test, ignore the statistics they give you, and use [Evan Miller's Awesome A/B Tools](http://www.evanmiller.org/ab-testing/) to determine when to stop the test. Go read all his [articles on the topic](http://www.evanmiller.org/), particularly [How Not to Run an A/B Test](http://www.evanmiller.org/how-not-to-run-an-ab-test.html).

Note also that in this post, I'm discussing fairly standard published bandit algorithms such as [Thompson Sampling](http://www.jmlr.org/proceedings/papers/v23/agrawal12/agrawal12.pdf) and [UCB1](http://jeremykun.com/2013/10/28/optimism-in-the-face-of-uncertainty-the-ucb1-algorithm/). There are techniques to resolve many of the issues I discuss within the bandit framework - unfortunately, many of these techniques are not published, and most of the ones I know of I've had to figure out myself.

# When a bandit algorithm is justified

To begin with I'll discuss some relatively standard bandit stochastic bandit algorithms. These include [Thompson Sampling](http://www.jmlr.org/proceedings/papers/v23/agrawal12/agrawal12.pdf) and [UCB1](http://jeremykun.com/2013/10/28/optimism-in-the-face-of-uncertainty-the-ucb1-algorithm/). These algorithms tend to be based on the following set of assumptions:

1. The samples drawn from each arm of the bandit are [Independent and Identically Distributed](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables).
2. The conversion rates for each arm do not change over time.
3. There is no delay between pulling an arm and observing the result. Or, more precisely, if there is a delay, it's shorter than the delay between opportunities to pull an arm.

If all these assumptions are known to be true, then using standard stochastic bandits is completely justified. Insofar as these assumptions fail to be true, standard stochastic bandits will stop working effectively.

There are other algorithms that make fewer assumptions, such as [Exp3](http://jeremykun.com/2013/11/08/adversarial-bandits-and-the-exp3-algorithm/). Due to their lack of assumptions, these algorithms tend to converge far more slowly, typically so slowly that they can *never be turned off*. Very few people tend to use them in practice, because they are optimized for the case when the [world is out to get you](http://jeremykun.com/2013/12/09/bandits-and-stocks/).

I should also mention that there are (in principle) stochastic bandit algorithms which can solve every issue presented here. However, if you know about such methods, it's probably because you developed them yourself - I don't know of any published material on this. If you did cook up your own bandits which violate the assumptions above, stop reading this post now.

**Note:** After writing the above, Noel Welsh pointed out a paper [Online Learning under Delayed Feedback](http://jmlr.org/proceedings/papers/v28/joulani13.pdf) which deals with one of these problems. I also know how to do it for Bayesian bandits, and [wrote it up a year after writing this post](https://www.chrisstucchio.com/blog/2016/delayed_reactions.html).

# Saturday is not Tuesday

The first problem using bandits in practice is the Saturday/Tuesday problem. Depending on what your website is selling, people will have a different propensity to purchase on Saturday than they have on Tuesday. Consider now an A/B test comparing following two headlines:

1. Happy Monday! Click here to buy now.
2. What a beautiful day! Click here to buy now.

It's intuitive to expect that headline 1 will have a higher conversion rate on monday, and a much lower conversion rate on other days. So suppose we run a bandit algorithm to determine this, starting on (for example) monday. We might observe the following results:

1. Mon: 1000 displays for "Happy Monday", 200 conversions. 1000 displays for "Beautiful Day", 100 conversions.
2. Tues: 1900 displays for "Happy Monday", 100 conversions. 100 displays for "Beautiful Day", 10 conversions.
3. Wed: 1900 displays for "Happy Monday", 100 conversions. 100 displays for "Beautiful Day", 10 conversions.
3. Thu: 1900 displays for "Happy Monday", 100 conversions. 100 displays for "Beautiful Day", 10 conversions.
4. More of the same.

Overall, it's pretty clear that "Happy Monday" is inferior to "Beautiful Day" - it's got a 20% conversion rate on Mon and a 5% conversion rate the rest of the week. That adds up to a 7.1% conversion rate, whereas "Beautiful Day" has a 10% conversion rate every day.

But it will take us a very long time to gather sufficient data to detect this! Because the bandit algorithm has almost converged to "Happy Monday", the number of samples displayed for "Beautiful Day" is very low. Thus it will take a lot of time for enough data to accumulate to counteract the mistake. After 11 days of running the bandit algorithm, we've gathered only 2,000 displays for "Beautiful Day" - 1,000 from day 1 and the remaining 1,000 from days 2-11.

## A/B tests have the same problem

Suppose we ran a 2 day A/B test, starting on Mon. We'd discover that "Happy Monday" had a 12.5% conversion rate compared to a 10% for "Beautiful Day". This result is simply unavoidable from any 2 or 3 day A/B test.

The only way to avoid this issue is to run the test for an integer number of weeks. I.e., if you start your test on Monday, you need to end the test on a Sunday. If you don't do this, you are potentially biasing your results by giving extra weight to certain days of the week.

# No one checks their email before 6AM

Delayed response is a big problem when A/B testing the response to an email campaign. The problem is the following. Suppose that Mon at midnight you've sent 1,000 "Beautiful Day" and 1,000 "Happy Monday" emails. Now it's 6AM, and it's time to send more emails.

You gather the data, and you discover that "Happy Monday" has had 2/1000 clicks while "Beautiful Day" has had 1/1000. This is very far from statistically significant. It suggests a nearly 0% conversion rate for all variants. Should we go back to the drawing board?

Of course not. At 6AM, most people are sleeping and haven't even bothered to check their email. They had no opportunity to click a link in an email. This is not a failure of the test, it's a failure of an assumption in the test. In real life, there is very often a delay between a display and a conversion. This will break a lot of algorithms.

# You don't get samples for free by counting visits instead of users

Dynamicyield is a company that sells bandit algorithms to companies attempting to increase their revenue, typically ecommerce sites. The recently discussed their algorithm in a [blog post](https://www.dynamicyield.com/2015/01/revenue-based-tests-2/).

Dynamicyield ran into the delayed response problem described above. Visitors would come to the site, fail to convert, but return days later and buy something. This causes a huge delayed observation problem - if a user visited 3 days ago, can we put them into the "did not convert" bucket? Maybe they will convert tomorrow?

According to their blog post, dynamicyield "solved" the problem in the following way. Instead of measuring things on a per-user basis, they measure things on a per-visit basis. Once a user is gone for 30 minutes (or some similar configurable amount of time), they are officially put into the "did not convert" bucket.

Here's the problem. Dynamicyield just fixed their delayed response problem but replaced it with a violation of [Independent and Identically Distributed](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables). Unfortunately, while user #1 and user #2 may behave in an uncorrelated way, visit #1 and visit #2 are correlated - visit #1 and visit #2 may both be coming from user #1!

Here's the problem.

Most bandit algorithms use the [Central Limit Theorem](https://en.wikipedia.org/wiki/Central_limit_theorem) to bound the variance of the samples. Once the variance of the sample is low, convergence has been achieved and the algorithm has converged. However, the variance of the Central Limit Theorem in the non-IID case is [vastly larger](https://en.wikipedia.org/wiki/Central_limit_theorem#CLT_under_weak_dependence) than in the IID case.

Based on some simple examples, supposing a single user visits the site 3x before buying, then the variance of the data set based on measuring visits rather than users might be `(1+2x3)=7` times larger than a naive algorithm would expect! (Note: to understand the details, see [this post](/blog/2015/no_free_samples.html).)

Without knowing further details about dynamicyield's implementation, it's not possible to figure out how strongly this affects their implementation. Since they are closed source, proving them right or wrong is impossible. But based on their lack of recognition of this problem on their blog, I'd suggest avoiding using them.

## A/B tests have a similar problem

The problem I described happens for A/B tests too. If you collect statistics on a per-visit basis rather than a per-user basis, your statistics are hopelessly correlated. You are getting a larger number of samples, and your tests will appear to converge in less time, but this is an illusion. Your tests haven't converged, you've merely increased N at the cost of increasing your variance.

The way to fix this is to make sure all your visitors have a sufficient amount of time to convert. For example, if 99% of your visitors convert after 1 week, then you need to do the following.

1. Run your test for two weeks.
2. Include in the test **only** users who show up in the first week. If a user shows up on day 13, you have not given them enough time to convert.
3. At the end of the test, if a user who showed up on day 2 converts more than 7 days after he first arrived, he must be counted as a non-conversion.

# Stick to A/B tests until you are an expert

None of these issues are, in principle, a problem for bandit algorithms. The issue of changing conversion rates can be handled by using [adversarial bandit algorithms](http://jeremykun.com/2013/11/08/adversarial-bandits-and-the-exp3-algorithm/). Changing conversion rates can also be handled by appropriate Bayesian techniques, and delayed observations can be handled similarly. (I'd link to appropriate techniques, but I've never seen them published. The ones I use, I had to develop myself.)

But if you don't recognize these issues up front and deal with them, they will make your bandit algorithms completely ineffective. This is not hyperbole - I've had a number of clients who have read my advocacy of bandit algorithms, blindly used them in code, and found them to be ineffective. This is probably my fault, and in retrospect I should have been more careful in my advocacy.

The simplest way to avoid these issues is to stick to basic A/B test methods. Run your tests for an integer number of weeks, track on a per-user rather than per-visit basis, and make sure all your users have enough time to respond. This is the most robust way to handle such things, and the only one I can recommend to any non-experts. My strong **recommendation** - if you can't follow the convergence proofs of bandit algorithms, you probably do not want to use them in your code. Bandit algorithms are great tools, but also very delicate and easy to get wrong.
