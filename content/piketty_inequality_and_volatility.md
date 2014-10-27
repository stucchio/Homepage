title: Piketty, inequality and volatility: How can r > g?
date: 2014-04-21 01:00
author: Chris Stucchio
tags: economics, macroeconomics, finance, volatility
mathjax: true





Thomas Piketty's new book, [Capital in the 21st Century](http://www.amazon.com/gp/product/067443000X/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=067443000X&linkCode=as2&tag=christuc-20)  has been making the rounds. Full disclosure: I have not yet read it.

According to all the reviews of the book, Piketty's fundamental conclusion is that `r`, the rate of growth of capital, exceeds `g`, the rate of growth of the economy over the long term. On it's face, this cannot possibly true since growth of capital is a portion of growth of the economy. If it has a higher growth rate over the long term, then eventually the `g` must become equal to `r`. However, I think I've found a solution to this puzzle - volatility.




# Why r > g is nonsense, for constant r and g

Suppose that $@ r $@ and $@ g $@ are both fixed quantities which do not change over time. We can do simple arithmetic to show that in the long term, $@ r $@ must equal $@ g $@.

The size of the total economy is equal to:

$$ E(t) = A e^{rt} + B e^{st} $$

We assume $@ r > s $@. The variable $@ g $@, the long term growth rate of the economy is:

$$ g = \frac{ \ln(E(t)) }{t} $$

This is straightforward to compute. First note that:

$$ E(t) = A e^{rt} + B e^{st} =  A e^{rt}(1 + (B/A)e^{(s-r)t}) $$

Therefore:

$$ g = \frac{ \ln(E(t)) }{t} = \frac{ \ln(A e^{rt}(1 + (B/A)e^{(s-r)t})) }{t} \\
= \frac{ \ln(A) + rt + \ln(1 + (B/A)e^{(s-r)t}) }{t} $$

$$ = r + \frac{ \ln(A) }{t} + \frac{ \ln(1 + (B/A)e^{(s-r)t}) }{t} $$

For large $@ t $@ both of the second terms become zero, implying that $@ g = r $@.

# How volatility changes things

To begin, I'm going to illustrate a mathematical fact. Suppose that we have a fixed rate of growth $@ g $@ over two time periods. Then if you start with 1 unit of wealth at time zero, at time 2 you have

$$ (1+g)(1+g) = 1+2g+g^2 $$

units of wealth. For example, if $@ g = 0.03 $@, after 2 time periods you have 1.0609 units of wealth.

Now suppose we have a variable rate of growth. At time 1, the growth rate $@ r $@ is 0.06. At time 2, the growth rate is 0. Over two time periods, the average growth rate is the same 0.03 as in the previous example. Yet:

$$ (1+2g)(1+0g) = 1+2g < 1+2g+g^2 $$

And in numerical terms, after two time periods, you only have $@ 1.0600 < 1.0609 $@ units of wealth.

This phenomenon is called [volatility drag](http://cssanalytics.wordpress.com/2012/03/12/understanding-the-link-between-volatility-and-compound-returns/). It means that not only does volatility increase your *risk*, but it actually lowers your long term *rate of return*.

## Quantifying Volatility Drag

Now lets alter the oversimplified model from above. Let's now assume that $@ s $@ is still constant, but $@ r(t) $@ varies. Specifically, let us suppose that:

$$ r(t) = r_0 + \sigma W_t $$

where $@ W_t $@ is a [Wiener process](http://en.wikipedia.org/wiki/Wiener_process). The long term value of an investment will then be given by:

$$ A \exp\left(\int_0^t r(t') dt' \right) $$

And by this token,

$$ E(t) = A \exp\left(\int_0^t r(t') dt' \right) + B e^{st} $$

You can use [Ito's lemma](http://en.wikipedia.org/wiki/It%C5%8D's_lemma#Geometric_Brownian_motion) to determine that:

$$ \int_0^t r(t') dt' = \left( r_0 - \frac{\sigma^2}{2} \right) t + \sigma B(t) $$

where $@ B(t) $@ is the current position of a Wiener process. Thus, the long term growth rate of capital is:

$$ \frac{\log\left[ A \exp\left(\int_0^t r(t') dt' \right) \right]}{t} = \left( r_0 - \frac{\sigma^2}{2} \right) + \frac{\sigma B(t)}{t} + \frac{ \ln(A)}{t}$$

Over the long term, $@B(t)$@ can be expected to be (most of the time) no larger than $@O(\sqrt{t})$@, so for large $@ t $@ both of the latter terms go to zero. Thus, we find that the long term growth rate of capital is $@ r_0 - \sigma^2/2 $@. Depending on how large $@ \sigma $@ is, this may be larger or smaller than $@ s $@.

# Capital accumulation

An important fact to recognize is that this *fundamentally changes* the story that Piketty wishes to tell in his book (at least according to the reviews of it). According to the reviews, Piketty claims that if $@ r_0 > g $@, then wealth will continue to accumulate in the hands of dynasties. But as shown above, volatility can destroy this accumulated wealth.

If you wish to critique my analysis by appealing to long tails and similar things (yes, I'm using a simple linear gaussian model), recognize that *long tails increase the effect of volatility*. For example, suppose the first generation of a dynasty is headed by Elon Musk (far out in the positive long tail), while the second generation is headed by a spendthrift who pisses away the family fortune (far in the negative long tail). Net result: no more dynasty.

# Important qualification

I haven't read [the book](http://www.amazon.com/gp/product/067443000X/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=067443000X&linkCode=as2&tag=christuc-20). For all I know, Piketty actually addresses these issues somewhere in the 700 page tome. But if he does, not a single review I've read of the book actually mentions it.

This doesn't surprise me too much - differences between the arithmetic and geometric mean seem a bit technical for the average innumerate reporter to even understand. But as is often the case, careful analysis gets in the way of an easy narrative. Those of us who are numerate should be careful to do a little math rather than relying on provocative verbiage, as nearly all the commentary on Piketty's book does.

**Hat tip:** The commenter "doug" over on [overcomingbias](http://www.overcomingbias.com/2014/03/hidden-taxes-must-be-huge.html) discussed this idea as well.

# Addendum (2014-04-25)

Apparently Piketty acknowledges that capital volatility is about [5-10x as large as income volatility](http://www.nationalreview.com/agenda/376345/thomas-piketty-made-case-privatizing-social-security-arpit-gupta). Because of this high volatility, he opposes turning wage earners into capital holders. Apparently what's good for the goose is bad for the gander, according to Piketty. I'm now very confused.

I've also started reading the book - just because you are writing a magnum opus doesn't mean you need to write 700 pages of low density anecdata with the actual point buried somewhere within. 150 pages in and still not a word about volatility, or even the micro-scale distribution.
