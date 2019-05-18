title: Wingify releases Bayesian A/B tester
date: 2015-10-01 09:33
author: Chris Stucchio
tags: ab testing, bayesian statistics
featured: true

<iframe width="560" height="315" src="https://www.youtube.com/embed/ofPEb-TSp08" frameborder="0" allowfullscreen></iframe>

I've written a number of posts here about a/b testing, and readers have probably observed that I favor the Bayesian approach. I'm very happy to announce that Wingify (my employer) has release SmartStats - a fully Bayesian A/B testing engine. I've always maintained that you should A/B test even if you won't do a good job - it's certainly better than flipping a coin.

But many people still make lots of mistakes - peeking at tests too often, changing the test halfway through, etc. Articles like [12 A/B Split Testing Mistakes I See Businesses Make All The Time](http://conversionxl.com/12-ab-split-testing-mistakes-i-see-businesses-make-all-the-time/) abound. We built SmartStats to help you avoid some of these problems. Specifically, SmartStats solves problems (1), (2), (3), (8) and (10) from Peep Laja's list via a combination of better statistics and UI warnings. (Point (5) on that list is [actually wrong](https://www.chrisstucchio.com/blog/2015/ab_testing_segments_and_goals.html).)

Go check out the [landing page](https://vwo.com/bayesian-ab-testing/) or the [venturebeat article](http://venturebeat.com/2015/10/01/wingifys-smartstats-ends-split-testings-most-common-problems/) to learn more.

(Obvious disclaimer: I work for Wingify. My endorsement is independent only insofar as  my contract includes a clause that allows me to withdraw my endorsement of any statistical snake oil.)
