title: The poor don't work because they are economically rational
date: 2011-05-12 00:00
author: Chris Stucchio
tags: poverty, economics



It's a fairly pervasive myth within the US that the poor work very hard at unpleasant jobs. But this is nothing but a myth - according to the BLS report [A profile of the working poor, 2009](http://www.bls.gov/cps/cpswp2009.pdf), as of 2009, only 24% of people below the poverty line were in the labor force (this means working or looking for work) for at least 27 weeks/year.

Out of these 24%, just under half work full time and another 20% are involuntary part time employed (i.e., they would like to work full time, but are only able to find part time employment) - see table 1 of [A profile of the working poor, 2009](http://www.bls.gov/cps/cpswp2009.pdf).

This means that in total, about 17% of people below the poverty line are willing to work full time for at least 27 weeks/year. If you exclude children from the numbers (number of poor children and children as a whole taken from [here](ftp://ftp.bls.gov/pub/special.requests/ce/standard/2009/income.txt), specifically Table Pop1 and Econ1.A.), then 36% of poor people work at least 27 weeks/year, and 25% work full time.

For comparison, for the population as a whole, 65% of people age 16 and older were in the labor force according to [BLS stats](http://data.bls.gov/timeseries/LNS11300000)].

This data begs the question - why don't the poor work? Are they simply irrational, choosing to live in poverty when they could do better? Do they simply have flat utility functions, and not care about goods and services above a low minimum threshold?

I propose an alternative hypothesis. I propose that the poor are economically rational.

I'll make the following assumptions:

Work provides a non-zero amount of disutility - all else held equal, the poor would rather not work than work. (This trait applies to most people - I don't know anyone who doesn't enjoy a day off.)
I propose that utility is a monotonic function of spending - this means that people prefer to increase the amount of goods and services they consume. A green piece of paper doesn't make me very happy, but the burrito I trade it for does.
If we accept these two assumptions, we can derive the following result: whenever the increased utility from *spending* does not outweigh the decreased utility from working, people will choose not to work. In particular, if increasing work does not increase spending, then people will choose not to work.

Now for some data (taken from the [BLS Consumer Expenditure Survey (for 2009)](ftp://ftp.bls.gov/pub/special.requests/ce/standard/2009/income.txt)):

![consumption graph](/blog_media/2011/why_the_poor_dont_work/spending_vs_earning.png)

On the X-axis I plotted earned income - the amount of money a person has earned via work or investment [5].  On the Y-axis, I plotted consumer expenditures. I also plotted spending vs earning in a theoretical world where income = expenditures.

The graph shows that utility (see Assumption 2) slightly decreases as you earn more money. People earning $5-10k actually spend $2k less than people earning $0-5k, and people earning $10-15k spend $1k less. By increasing your earned income to $20k, you still only get to spend $1000 more than if you didn't work.

So this presents you with a tradeoff. You can have no job, consume leisure in your free time, and your expenditures will be $22731. You can have a job and consume less leisure, and you'll only get to spend $23706. This means that if your work opportunities pay only $20k/year, every hour spent working only allows you to spend 97 cents. If the $20k/year job is actually 35 hours/week, then each hour spent working only enables 56 cents worth of expenditures.

In fact, even if you could increase your wages to $30k/year, you would only get to spend about $3.80 per hour worked (again assuming a 35 hour work week)

This means that it is completely rational for any person who values their time at more than $0.56-3.80 not to work as long as their work opportunities pay less than $30k/year.

Economic rationality seems to be a plausible explanation for the work habits of the poor.


### A note on coding

For each interval, I chose the x-coordinate to be the midpoint. E.g., the interval $5-10k is coded as $7.5k. The top interval ($70k+) is coded as $85k.

**Update, as of Jan 17 2014:** Turns out my rough calculations were in the [right ballpark](/blog/2014/why_the_poor_dont_work_redux.html). Apparently a year after I wrote that the CBO did more careful calculations, and they are in general agreement. [CBO report](http://www.cbo.gov/sites/default/files/cbofiles/attachments/11-15-2012-MarginalTaxRates.pdf) and John Cochrane's [blogspam version](http://johnhcochrane.blogspot.co.uk/2012/11/taxes-and-cliffs.html).
