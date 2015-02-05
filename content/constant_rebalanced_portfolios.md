title: Constant Rebalanced Portfolios - some simulations with numpy
date: 2015-02-05 10:00
author: Chris Stucchio
tags: economics, trading, portfolio theory
category: trading


I've had several discussions with friends lately about investing, mostly in the wake of robinhood.io's early release. Quite a few people have the plan to put some cash into robinhood.io accounts and engage in some sort of investment strategy. Strategy ideas range from daytrading (I do NOT recommend this) to buy&hold. One notable strategy that not a single person has discussed is the *constant rebalanced portfolio*, and I think it's important to get word of such theories out there.

A buy&hold strategy consists of buying a set of securities at time t=0 and holding them until some date in the distant future. For example, one might purchase shares of [SPY](https://www.google.com/finance?q=spy&ei=ITrTVKHIHNPaqQHXrYHwAg), [VHT](https://www.google.com/finance?q=vht&ei=MDrTVKmKFIuNrQHdwoHIDQ) and [VDE](https://www.google.com/finance?q=NYSEARCA%3AVDE&ei=KDrTVNmLOIXUqQHlrYH4Bw) and then hold them for a long time. Another possibility is the constant rebalanced portfolio, which I'll describe shortly.

Lets play with Python a bit to get an idea of how various strategies will perform.

```python
num_periods = 10 #
num_securities = 3 # 3 securities
r = norm(1.1, 0.1).rvs((num_periods,num_securities))
# Example output:
# array([[ 1.266567  ,  1.21155283,  1.06577593],
#        [ 1.115565  ,  1.17878424,  1.22573429],
#        [ 1.24932466,  1.18716934,  1.02244259],
#        ...
#        [ 1.04909711,  1.1380544 ,  1.06287509],
#        [ 1.07807363,  1.02156611,  0.99188715]])
```

# Buy and Hold

Suppose now we have a fixed amount of money - say $1.00. We might allocate this cash between each security in some way - say 1/3 for each symbol. How much money will we gain at the end?

The return for each symbol over 10 years can be computed as follows:

```python
per_symbol_return = prod(r, axis=0)
# array([ 2.85671627,  2.63321033,  2.96514375])

apr = power(per_symbol_return, 12.0/num_periods)
# array([ 1.11067427,  1.10166247,  1.11481955])
```

So each symbol is averaging a 10-11% rate of return per period, as we would expect given the way we generated it.

To compute the returns from a buy&hold portfolio, we simply take the dot product of our portfolio allocation with the rate of return:

```python
allocation = ones(num_securities)/num_securities
# array([0.33, 0.33, 0.33])
total = dot(per_symbol_return, allocation)
# 2.79
total_apr = power(total, 1.0/num_periods)
# 1.108
```

So a buy&hold strategy is achieving a 10.8% APR for us.

![](/blog_media/2015/constant_rebalanced_portfolios/buy_and_hold.png)

# Constant rebalanced

The constant rebalanced portfolio takes the following approach. Suppose some particular symbol performs well in period 1 - we assume this is likely to be due solely to random chance (perhaps due to the [Efficient Markets Hypothesis](https://en.wikipedia.org/wiki/Efficient-market_hypothesis)). After we've achieved this windfall return in, say, SPY, our opinion that the best portfolio allocation is [1/3,1/3,1/3] hasn't changed.

So suppose our portfolio allocation started at [1/3, 1/3, 1/3], but changed to [1/2, 1/4, 1/4] after SPY achieved disproportionate returns. At this point we rebalance our portfolio by selling off excess SPY and buying up VHT and VDE until our portfolio allocation is again [1/3, 1/3, 1/3].

Lets calculate the returns we achieve this way.

```python
per_period_return = dot(r, allocation)

cumulative_return = prod(dot(r,allocation))
# 2.85
total_apr = power(total, 1.0/num_periods)
# 1.11
```

So we've increased our gains simply by 24 basis points by rebalancing.

![](/blog_media/2015/constant_rebalanced_portfolios/const_rebal_vs_buy_hold.png)

# Dealing with transaction costs

One problem with rebalancing a portfolio is that it often incurs a hit on transaction costs. Robinhood.io allows free trading, but one doesn't escape from paying the spread. Even worse is the tax hit.

In practice, for everyday investors, the best way to avoid transaction costs is to rebalance only when adding funds. A typical investor, including all my friends who just got their robinhood.io invites, will be adding a fixed amount of money (perhaps $500) to their brokerage account each month.

So if one's target allocation is [1/3, 1/3, 1/3], but the actual allocation is [1/2, 1/4, 1/4], then the best way to rebalance will be to add new funds (e.g. the extra $500/month) to the second and third components until balance is achieved.
