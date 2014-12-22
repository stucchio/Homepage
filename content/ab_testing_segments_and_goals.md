title: Segmenting your traffic? You are probably doing it wrong.
date: 2015-01-05 09:30
author: Chris Stucchio
tags: ab testing

So you've jumped onboard the A/B testing bandwagon. You've just run an A/B test comparing the site redesign to the old version. Unfortunately the redesign did not differ in a statistically significant way from the old version. At this point, a variety of [conversion rate experts](http://online-behavior.com/targeting/segment-or-die-214) will tell you to [segment your data](http://conversionxl.com/how-to-build-a-strong-ab-testing-plan-that-gets-results/):

> An experiment that seemed to be performing poorly might have actually been successful, but only for a certain segment. For example, our experiment may have shown that a variation of our mobile landing page is not performing well. When looking into the segments though, we may see that it is performing exceptionally well for Android users, but badly for iPhone users. When not looking at segments, you can miss this detail.

This is an intuitively natural idea - everyone is different, so why isn't it possible that one version will perform worse for some groups than another? As a data geek, it also gives us the opportunity to play with Pandas or Excel and build an impressive presentation to show our boss.

**Resist the urge to do this!**

Suppose you ignore my advice. You've decided to segment your users and look for interesting results. I can virtually guarantee that if you put enough effort in, *you will find* statistically significant correlations. Maybe your visitors using Android from Oklahoma (all 58 of them) have a significantly higher conversion rate on the redesign than on the original site.

How can I guarantee that you'll see something interesting even if there is nothing there? Because of the [multiple comparisons problem](https://en.wikipedia.org/wiki/Multiple_comparisons_problem).

# Multiple comparisons - a review

Suppose you run statistical tests with a p-value cutoff of 5%. What this means is that if you were to repeatedly run an A/A test (a test comparing the control group to itself), you would expect 5% of your tests to return a statistically significant value. In essence, the P-value cutoff is the false positive rate you've decided is acceptable.

So now lets think about how many segments you have. You've got mobile and desktop, 50 states, and perhaps 20 significant sources of referral traffic (google search, partner links, etc). All told, that's 2 x 50 x 20 = 2000 segments. Now lets assume that each segment is identical to every other segment; if you segment your data, you'll get 0.05 x 2000 = 100 *statistically significant* results purely by chance. With a little luck, Android users in Kentucky referred by Google, iPhone users in Nebraska referred by Direct and Desktop users in NJ all preferred the redesign. Wow!

Here is an actual picture taken from an [article advocating segmentation](http://online-behavior.com/targeting/audience-segmentation):

![segmentation](http://online-behavior.com/sites/default/files/imagecache/Content/articles/Segmentation-Analysis-report.jpg)

The largest of those segments has 100 visitors! You simply do not have enough data to determine whether searches for "ninja" or "crepuscular light" will result in more conversions. Sorry, you are out of luck. Stop segmenting and don't try again until you've increased your traffic by 100x.

# Multiple goals - the same problem applies

A lot of people, in addition to segmentation, like to track multiple goals on their site. For example, newsletter signups, add item to shopping card, or save item for later. Congratulations - by using multiple sufficiently many goals, you'll definitely find a statistically significant result in one of them.

This effect is partially mitigated if your goals are correlated with each other. I.e., if people who sign up for the newsletter also tend to add an item to the shopping cart, then the issue of multiple goals is reduced. On the other hand, the more your goals are correlated with each other, the less useful information you actually get out of tracking multiple goals .

## How to fix the problem of multiple goals

Ok, you are still determined to segment your traffic. Now it's time for [one weird trick](https://en.wikipedia.org/wiki/%C5%A0id%C3%A1k_correction) to use to avoid running into the problems I've described above. It's a simple formula you can use. Suppose you want to run a segmented test with a p-value cutoff of 0.05. You can use the following formula to compute a *new* cutoff that works with multiple segments:

    new_p_cutoff = 1 - (1 - old_p_cutoff)^(1/number_of_segments)

According to this formula, if we have 20 segments, `new_p_cutoff=0.00256`. So suppose you've run a test with 20 segments. If you want to have a 5% chance of observing a false positive in the test, then you must declare any individual test to be statistically insignificant unless it yields a p-value smaller than 0.00256.

You can use the same formula with multiple goals as well. This formula is called the [Sidak Correction](https://en.wikipedia.org/wiki/%C5%A0id%C3%A1k_correction), by the way.

It's possible your A/B testing tool has this built in, but you should not take that as a given.

# Experimenter degrees of freedom

This problem is trickier to fix. Experimenter degrees of freedom come into play when determining *what to test*. When looking for something interesting, one might first try segmenting by browser. When that fails, one might then try segmenting by location, and if that fails by demographic. The first test involves segmenting 5 ways, so the experimenter will plug `number_of_segments=5` into the Sidak Correction above. The second test involves 50 segments, so the experimenter plugs `number_of_segments=50` into the formula.

Look kosher? It's not.

The problem is that by the time the experimenter finished segmenting by browser, *he already had a 5% chance of seeing a false positive*. The second segmentation attempt introduced *another* 5% chance of making an error. So the data analyist now has a 10% chance, rather than a 5% chance, of seeing a false positive!

## How to reduce experimenter degrees of freedom

The only way to avoid this problem is *preregistration*. Before you look at the data, decide how many segmentation attempts you will make. Ask yourself: "Self, hypothetically, if segmenting by browser doesn't give anything interesting, what will I do next?" Once you've decided this, you must then count the number of segments *from every attempt you might possibly make*.

So in the above example, `number_of_segments = 5 + 50 + 25` (assuming 5 browsers, 50 geographic locations and 25 demographic segments). That's the easy part.

The hard part is to *stop* after you've done it all. At this point, you failed. No matter how you kick the data around, you'll only be obtaining statistically significant results by chance.

Andrew Gelman discusses this in a lot more detail in his article, [The Garden of Forking Paths](http://www.stat.columbia.edu/~gelman/research/unpublished/p_hacking.pdf).

# But Google and Amazon make $hitton$ of money by segmenting and personalizing?!?

Google and Amazon have more traffic than you.

# Conclusion

Lots of people on the internet are suggesting that you should segment your A/B testing data in order to understand things more deeply. Unfortunately, none of these people are telling you how to do it correctly. Segmentation is hard. Most of the time it doesn't give you anything useful. But unless you are very careful, of all the false positive will make it look like segmentation generated a big win.
