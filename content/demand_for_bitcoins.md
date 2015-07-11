title: What is the correct price for a (crypto or other) currency?
date: 2014-02-20 08:00
author: Chris Stucchio
tags: economics, bitcoin, macroeconomics





A [lot](http://www.forbes.com/sites/jessecolombo/2013/12/19/bitcoin-may-be-following-this-classic-bubble-stages-chart/) [of](http://ordinary-gentlemen.com/blog/2013/12/12/these-three-graphs-prove-that-bitcoin-is-a-speculative-bubble) [people](http://kottke.org/13/12/is-bitcoin-a-speculative-bubble) believe that Bitcoin and other cryptocurrencies are a speculative bubble. Scott Sumner is a notable person who [disagrees](http://www.themoneyillusion.com/?p=25011), and believes that Bitcoin may be rationally priced based on the low probability of high expected rewards.

Most of the arguments claiming BTC is a bubble are nonsensical. They tend to fall into two categories: "OMFG prices went sky high, must be a bubble", and "BTC, like the USD, has nothing backing it, therefore it must be a bubble" (some of the latter critics recognize that USD has the same problem, others do cognitive dissonance). I'm not going to address the question of whether BTC is a bubble, because I don't actually understand things well enough to give an answer.

Instead, I'm going to describe how to use mainstream textbook macroeconomic theory to determine the "true price" of BTC. So you can think of it as a tutorial for speculating on Bitcoin - assuming you can predict the future, I'll give you a set of formulas you can plug your predictions into. Then you can use the formulas to determine the "true price" of BTC and speculate on that basis - if the "true price" is higher than the current price, you should buy, otherwise sell (or short).



**Important note:** I'm not going to provide any *trading strategies* in this post. If I had a trading strategy that I believed in, I'd put my money where my mouth is (anyone who refuses to do the same is full of crap). I'm merely explaining how to turn *predictions* like "bitcoin transaction costs will go down" or "bitcoin transactions will drastically increase" into a trading strategy.

# Why do people want money or bitcoins?

Fundamentally, this is the important question to answer. Let's think about all the unpleasant properties of money (paper cash). It tends to bear a negative interest rate, or at best (in the case of BTC) has a long term interest rate of zero. In the case of physical money it's a pain to carry around and it can be damaged. In the case of cryptocurrencies you need to maintain a wallet and protect yourself from hackers. As far as preserving the value of my wealth, there are far better options - SPY, for example.

In theory, I should have no reason to hold Dollars, Pounds, Rupees or Bitcoins.

So lets put this theory to the test. What's in my wallet?

![Picture of Ghandi](/blog_media/2014/demand_for_bitcoins/ghandiji.jpg)

I've also got a few hundred GBP and a few hundred USD floating around. I guess that theory is now debunked. So why am I carrying all this paper? One very simple reason.

**Auto drivers don't accept credit cards.**

I need to carry currency to perform my everyday transactions - getting laundry done, taking an auto, buying a dosa, etc. For this very important reason, I'm willing to store some of my wealth in the form of flimsy little pieces of paper which will earn me a rate of return of approximately -10%.

So we arrive at the first fundamental principle of currencies. If people need to perform transactions with a currency then that currency will have a positive value.

## Mathematically Modelling the Demand for Money

In order to do everyday transactions, people want to hold an inventory of currency. The important question to answer is "how much?" I have a few thousand Rupees in my pocket, but that's far less than my life savings. I have a lot more wealth invested in SPY, USD, and various interest-bearing USD-denominated securities. So how can we determine how much money I put into Rupees?

The [Baumol-Tobin model](http://en.wikipedia.org/wiki/Baumol-Tobin_model) provides a good way to think about things. It's not a perfect model, but it provides a useful way to think about things. The basic idea is that people hold an inventory of currency to minimize transaction costs. If I want to convert from USD to INR, I need to take an auto to an ATM and then pay my bank a foreign transaction fee. Even if I were in the US, there would still be labor involved in holding enough cash.

On the other hand, I don't want to hold too much cash. Every year, the value of those pictures of Ghandi in my pocket go down by 10% or so. Furthermore, I lose the opportunity cost of putting rupees into an interest bearing account - I believe a savings account over here will yield a nominal 6%.

So the amount of cash I want to have on hand, assuming I'm making optimal decisions, can be arrived at by minimizing the sum of transaction costs and opportunity costs. The Baumol-Tobin model does this for one patricular model of transaction costs, and arrives at the following equation for monetary demand:

    M(P) = P sqrt(C Y / 2 R)

In this equation, `P` is the price level, `C` is the transaction costs, `Y` is real consumption, and `R` is interest rates.

So the key qualitative facts are the following:

**First:** higher transaction costs mean people want to hold more money.

**Second:** higher price levels and higher consumption mean people want to hold more money.

**Third:** higher interest rates mean people want to hold less money.

# Computing the Bitcoin Price Level

Although this is macroeconomics, we can still use a supply&demand curve. But instead of using *price* as one of the axes, we use *price level*.

For BTC, the supply (in the long run) is pretty easy to figure out - 21 million. There is of course a small probability that the Bitcoin system will collectively agree to allow inflation or a different number, but I'll ignore this for the moment.

For USD, it's much more difficult. To figure out money supply, you need to guess the actions of the Federal Reserve over the long term. Since this post is about speculating on BTC, I won't bother to get into that.

So the game to be played is matching the supply and demand curves. In pictures, it means finding the point where the two curves intersect:

![Supply and demand](/blog_media/2014/demand_for_bitcoins/supply_and_demand.png)

In equations, it means solving the equation:

    21e6 = P sqrt(C Y / 2 R)

The solution is:

    P = 21e6 sqrt(2R/CY)

It's important to note that all the quantities I'm listing here apply *to the bitcoin economy only*.

Also, just so that we keep track of what this means in real world terms, a *higher* price level means that bitcoins are *less* valuable. So a more useful quantity to think about might be:

    1/P = (1/21e6) sqrt(CY/2R)

This is the *value* of bitcoins - it represents the real goods that a bitcoin can buy you in the future. So you want to go **long** if you expect `1/P` is large and **short** if you expect it to be small.

# What Macroeconomics tells us about demand for Bitcoins

The first thing to note is that the larger the bitcoin economy is in real terms (goods and services, represented by `Y`), the more valuable bitcoins become. This is rather unsurprising. If no one uses bitcoins for anything, they are worthless, while if everyone uses them they are more valuable.

The second and somewhat surprising fact is that the higher transaction costs are, the more valuable bitcoins are. But I'll try to give an intuitive explanation. In the US I carry very little cash. I can pay for nearly anything with a credit card, and then pay off my revolving debt (i.e. turn interest bearing bank deposits into cash) at the end of the month. In India, I carry a lot - credit cards are nearly useless here, due to the higher transaction costs (I need to pay foreign transaction fees).

Of course, this second fact is true only holding everything else in isolation. If transaction costs drop precipitously, it is likely that people will shift spending from dollars to bitcoins. This would result in a corresponding increase in Y. So although `C` might fall, `CY` (and hence `1/P`) could actually increase as a result.

The last key property is that higher interest rates make bitcoins less valuable.

# It's difficult to make predictions, especially about the future

To engage in financial speculation, you need to be able to predict the future. To determine the price level of BTC, we ultimately need to predict interest rates, transaction costs and real BTC-denominated consumption. This is hardly a trivial matter, but ultimately speculation is about predicting the future and then making bets on it.

Once you have a predictive model of `C`, `Y` and `R`, you run it and plug the result into the formula for `1/P`. This will tell you the real value of bitcoins in the future. You can then compute an exchange rate between BTC and Dollars/Rupees/etc, compare market prices to your own speculative price, and trade appropriately.

# See also

In a previous post, I discussed the macroeconomics of [Bitcoin's deflationary nature](http://www.bayesianwitch.com/blog/2014/bitcoin_critics_not_even_wrong.html).

I recommend reading [Macroeconomics](http://www.amazon.com/gp/product/0716752379/ref=as_li_ss_tl?ie=UTF8&amp;camp=1789&amp;creative=390957&amp;creativeASIN=0716752379&amp;linkCode=as2&amp;tag=macrolink1-20) in order to learn more about monetary theory and macroeconomics. You can buy an older edition slightly used [for only $9.50](http://www.amazon.com/gp/product/0716752379/ref=as_li_ss_tl?ie=UTF8&amp;camp=1789&amp;creative=390957&amp;creativeASIN=0716752379&amp;linkCode=as2&amp;tag=macrolink1-20).
