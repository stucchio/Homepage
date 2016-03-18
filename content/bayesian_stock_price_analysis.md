title: Bayesian time series analysis - analyzing stock prices
date: 2016-3-17 08:45
author: Chris Stucchio
tags: statistics, bayesian reasoning, trading
mathjax: true
category: trading


One very important use case of timeseries analysis is studying stock prices - in fact, that is probably the disproportionately most common use case. The basic idea is that given a timeseries - say `SPY(t)` - observable up to a certain time (today), can we predict in some sense what it will look like in the future?

As I discussed in an [earlier post](/blog/2016/has_your_conversion_rate_changed.html), Bayesian timeseries analysis is a great way to analyze such problems. Given an underlying predictive model, Bayes rule provides a way to compute posteriors on the model parameters. But once we have that, how do we make predictions about the future? It turns out that an important algebraic property of probability distributions - namely that probability is a [monad](https://en.wikipedia.org/wiki/Monad_(functional_programming)) - comes into play and makes this pretty easy.

For the most part the framework I describe here is how I trade. I formulate a model, do some Bayesian analysis on it, and then make trading decisions on that basis. However, for [obvious reasons](https://en.wikipedia.org/wiki/Efficient-market_hypothesis), the strategy I'm describing here won't work. It's designed to be really simple to explain - the principle is take a simple model and use Bayesian methods to analyze it so that the reader can understand the Bayesian part of the story. There are no shortage of other sources which describe all sorts of modes of stock price analysis that take more common maximum likelihood type approachs.

Lastly, I do recommend that the reader [go back and read part 1](/blog/2016/has_your_conversion_rate_changed.html) of this series.

## Stock prices

At the heart of any trading scheme is a statistical model - a mathematical rule describing, at least probabilistically, how stock prices behave. The probabilistic bit is important here. Let me explain this distinction in concrete programmer terms.

A function `predict: PastData => (Time => Price)` is a deterministic predictor - it looks at past data and outputs a single function mapping time to stock price. This single function is it's prediction of how a stock price will behave in the future.

A function `predict: PastData => Prob[Time => Price]` is a probabilistic predictor. It looks at past data and outputs a *probability distribution* over possible future stock price trajectories.

(In an actual programmatic implementation, `Time` and `Price` might both be long integers or something similarly simple. I'm just writing it this way for pedagogical purposes.)

The predictor we'll try to compute will be a probabilistic one.

The model I'm going to take is a fairly simple one - piecewise linear stock price movements. Specifically, let $@ s(t) $@ be a stock price. I'll assume:

$$ s(t) = s(t_0) + b_0 t + g_t, t_0 < t < t_1 $@
$$ s(t) = s(t_1) + b_1 t + g_t, t_1 < t < t_2 $@
etc

Here $@g_t $@ is a noise term. So what this model assumes is that the stock prices moves along a noisy straight line from time $@ t_0 $@ to $@ t_1 $@, then it moves along a *different* straight line from $@ t_1$@ to $@ t_2 $@, etc. Here's an example of a simulated timeseries according to this law:

![simple model](/blog_media/2016/bayesian_stock_price_analysis/simple_model.png)

The blue line illustrates the linear motion, and the green line illustrates the true stock price.

There are two parts of this model which are currently unspecified - what is $@ g_t $@, how to choose $@ b_i $@ and also how the times $@ t_1, t_2, \ldots $@ are chosen. A more or less obvious choice would be to let $@ g_t $@ be a [Brownian motion](https://en.wikipedia.org/wiki/Brownian_motion) or perhaps an [Ornstein-Uhlenbeck process](https://en.wikipedia.org/wiki/Ornstein%E2%80%93Uhlenbeck_process). The times $@ t_i $@ can be determined by simply assuming a fixed probability distribution on $@ \delta t_i = t_{i+1} - t_i $@.

So python code to generate a timeseries might look something like:

```python
from scipy.stats import norm, poisson

def gt(n):
    return cumsum(norm(0,1).rvs(n))

def dt():
    return poisson(50).rvs()

def bi():
    return norm(0,1).rvs()

def gen_series(N, start_price=10.0):
    x = zeros(shape=(N,), dtype=float)
    start_pos = 0
    while (start_pos < N):
        d = dt() #A float
        endpoint = min(start_pos+d, N)
        g = gt(endpoint - start_pos) #An array of length endpoint - start_pos
        b = bi() # A float
        if (start_pos == 0):
            x[start_pos:endpoint] = start_price + b*arange(0,endpoint - start_pos) + g
        else:
            x[start_pos:endpoint] = x[start_pos-1] + b*arange(0,endpoint - start_pos) + g
        start_pos = start_pos + d
    return x
```


### Data

To begin, all the data I I'll be using is available via [Quandl](https://www.quandl.com). There are docs on using [quandl from python](https://www.quandl.com/help/python).

```
In [1]: import Quandl

In [3]: Quandl.get("GOOG/NYSE_SPY", authtoken='hahasuckers')
Out[3]:
              Open    High     Low   Close     Volume
Date
1997-08-21    0.00   94.25   92.09   92.59    5392600
1997-08-22    0.00   92.73   90.56   92.56    7172900
...            ...     ...     ...     ...        ...
2016-03-15  201.36  202.53  201.05  202.17   93169090
2016-03-16  201.60  203.82  201.55  203.34  129303179

[4685 rows x 5 columns]
```


Yay, Quandl!
