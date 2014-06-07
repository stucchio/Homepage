title: A High Frequency Trader's Apology, Pt 1
date: 2012-04-16 10:00
author: Chris Stucchio
tags: economics, trading, high frequency trading
category: high frequency trading





I'm a former high frequency trader. And following the tradition of [G.H. Hardy](https://en.wikipedia.org/wiki/G._H._Hardy), I feel the need to make an [apology](https://en.wikipedia.org/wiki/A_Mathematician's_Apology) for my former profession. Not an apology in the sense of a request for forgiveness of wrongs performed, but merely an intellectual justification of a field which is often misunderstood.

In this blog post, I'll attempt to explain the basics of how high frequency trading works and why traders attempt to improve their latency. In future blog posts, I'll attempt to justify the social value of HFT (under some circumstances), and describe other circumstances under which it is not very useful. Eventually I'll even put forward a policy prescription which I believe could cause HFT to focus primarily on socially valuable activities.




Also, after you are done reading, go read the [HN Comments](http://news.ycombinator.com/item?id=3852341). Many of them are excellent. In particular, some clarification and correction is made to what I've posted - e.g., [Midpoint Passive Liquidity](http://usequities.nyx.com/markets/nyse-arca-equities/order-types) orders are discussed, which is a partial exception to my talk of the subpenny rule.

## Mechanics of HFT

Any serious discussion of HFT needs to begin with an explanation of the mechanics of how HFT works. The fundamental object in HFT (or exchange-traded securities in general) is the order book. Suppose Mal comes along and wishes to purchase some shares of Blue Sun. He'll probably have in mind some quantity he wishes to purchase, and he probably has some maximum price in mind. So Mal approaches a matching engine (e.g., [ARCA](http://www.nyxdata.com/page/1084), [BATS](http://batstrading.com/)) and places his order there:

    BUY(owner=Mal, max_price=20.00, quantity=100)

At this point Mal hasn't bought or sold anything - he has merely informed the world of his desire to buy. The matching engine takes his order and displays it (anonymized) to all other traders with a data feed.

Now suppose Inara comes along and wishes to sell some shares, say 200 shares @ $20.10. She places her orders, and it is again displayed to the world (anonymously) and stored. The order book now looks like this:

    SELL(owner=Inara, min_price=20.10, quantity=200)
    ------
    BUY(owner=Mal, max_price=20.00, quantity=100)

At this point, no trades have occurred - Mal is only willing to give $20 or less, Inara is only willing to receive $20.10 or more, so no trade occurs. At this point the market has created a bid/ask spread of $0.10 = $20.10 - $20.

Lets continue the example. Suppose now a few more people place orders - suppose Kaylee places an order to sell 200 shares @ $20.21 and River places a sell order for 100 shares @ $20.10. These orders are also stored.

Finally, suppose Simon comes along and places a buy order for 250 shares @ $20.21. He would be happy to trade with Inara, Kaylee or River - all are willing to sell at a price less than or equal to $20.21. The matching engine uses two primary rules to determine whether who will trade:

- Price. The best price always wins.
- Time. If the price is equal, then whoever placed their order first wins.

So at the moment before Simon's order is placed, the order book looks like this:

    SELL(owner=Kaylee, min_price=20.21, quantity=200) <- Trades third
    SELL(owner=River, min_price=20.10, quantity=100) <- Trades second
    SELL(owner=Inara, min_price=20.10, quantity=200) <- Trades first
    ------
    BUY(owner=Mal, max_price=20.00, quantity=100)

When Simon places his order, the matching engine will match it as follows:

- Simon buys 200 shares from Inara at price $20.10. Simon trades with Inara before River because Inara was the first to place her order.
- Simon buys 50 shares from River at price $20.10 because River offers a lower price than Kaylee.

Simon has now bought 250 shares, just as he desired.

At the end of this process, the order book then looks like this:

    SELL(owner=Kaylee, min_price=20.21, quantity=200)
    SELL(owner=River, min_price=20.10, quantity=50)
    ------
    BUY(owner=Mal, max_price=20.00, quantity=100)

Because Kaylee isn't willing to offer a good price, her order goes unfilled. Poor Kaylee. Oh well, if she is sad, I'll [feed her strawberries](http://www.youtube.com/watch?v=bYopf8KSy4o) to comfort her.

Anyway, this is the basic mechanics of trading.

There are many more details, of course, and far more order types than merely limit orders. But limit orders are sufficient for this blog post.

You can learn more by reading [Trading & Exchanges](http://www.amazon.com/gp/product/0195144708/ref=as_li_ss_tl?ie=UTF8&tag=christuc-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=0195144708) or [Algorithmic Trading & DMA](http://www.amazon.com/gp/product/0956399207/ref=as_li_ss_tl?ie=UTF8&tag=christuc-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=0956399207) (DMA stands for Direct Market Access), though neither book covers things in that much detail. Eventually, you just need to dig into the docs given out by matching engines, see [ARCA](http://usequities.nyx.com/markets/nyse-arca-equities/order-types) or [INET](http://www.nasdaqtrader.com/Trader.aspx?id=TradingUSEquities) for example.

### Market Making

Most HFTs run a market making strategy. What this means is they play both sides of the table - they take no position on whether a stock will go up or down. Instead, they try to offer securities both to buy and sell. If you want to buy, they will sell to you at $20.10. If you want to sell, they'll buy from you at $20. As long as their buys and sells match don't get too out of whack, the HFT will collect $0.10 = $20.10 - 20.00.

Of course, the market maker takes on risk - he might buy at $20 and then watch the stock tank. If he buys at $20, and the stock goes to $15 before he can sell, he just lost $5. So the market maker needs to balance risk with reward - if he sets the bid/ask spread too low, he will lose money, while if it's too high, no one will trade with him.

It's important to note that market making is nothing new. In the era when stocks were traded in 1/8ths and 1/16ths, market making was done by humans working in [the pit](https://en.wikipedia.org/wiki/Trading_pit). A single human trader would often run a market making strategy on larger stocks with significant volume. Later on, from the 1980's to the early 2000's, human daytraders would often fill this role. To a much lesser extent they still do.

Automated trading systems have replaced these human market makers for a very good reason - cost. For a strategy (and note: this strategy works only for a few securities, no human can track hundreds of stocks mentally) to be worth a financial professional's time and effort, it must generate at least $20-200k profit each year (this assumes a human smart enough to daytrade would work for $20k/year). In contrast, a single server in a data center can run hundreds of strategies at a cost closer to $50k/year, and they can do it faster and more accurately than any human.

The rise of algorithmic trading is merely a special case of machines replacing humans. Traders are no more immune to this than factory workers.

## Latency and Order Flow

For market makers, the name of the game is order flow. As long as your buys and sells are well matched (i.e., every time you buy, you also sell), your profit is going to be proportional to

    (# of shares traded) x (ASK PRICE - BID PRICE).

The constant of proportionality depends mainly on the skill of the high frequency trader at guaging the risks.

Basically the more you trade, the more money you make (all else held equal). So how can a market maker trade more?

The answer is that he needs to be close to the top of the order book. As we saw in our previous example, Inara traded more than River, and River traded more than Kaylee. The simplest way to reach the top of the order book is to offer the best price. Supposing Jayne wants to jump to the top of the queue on the buy side, he needs to offer a better price than Mal:

    SELL(owner=Kaylee, min_price=20.21, quantity=200)
    SELL(owner=River, min_price=20.10, quantity=50)
    ------
    BUY(owner=Jayne, max_price=20.05, quantity=100) <-   Jayne offers a better price
    BUY(owner=Mal, max_price=20.00, quantity=100)        than Mal, so he will trade first.

Of course, there is a balance to be struck. Since Jayne will only be earning $0.05/share traded, he needs to make sure this reward outweighs the risks. Let us suppose that the border between expected profit and loss is $20.05 - that is to say, there is not a single market participant who believes he can make a profit by offering more than $20.05. In that case, Jayne will always trade first, since he placed his order earliest.

This fact shows why speed matters. Suppose that at precisely 10:31:30:000 AM, new information becomes available which suggests that it will now be profitable to place a buy order at $20.07 - perhaps a press release has hinted that the price will go up, or a correlated security has just gone up in price. Because of this, both Mal and Jayne want to change the price on their orders to $20.07. Whoever happens to be fastest will rise to the top of the book:

    SELL(owner=Kaylee, min_price=20.21, quantity=200)
    SELL(owner=River, min_price=20.10, quantity=50)
    ------
    BUY(owner=Mal, max_price=20.07, quantity=100) <- received at 10:31:30:427
    BUY(owner=Jayne, max_price=20.07, quantity=100) <- received at 10:31:30:639, 212ms too late

This is why automated market making has morphed into high frequency trading, and why so much effort is poured into creating low latency systems. Whoever places their order first will be the most likely to trade.

A second reason why speed is important is because when the market moves, traders often wish to cancel their orders. At 10:31:30:000, an event occurred which suggested the price of the security will go up. It is likely beneficial for River to cancel her sell order at price 20.10 and raise it to $20.20. Conversely, after this event, it might also be beneficial for another trader (say Wash) to pounce on her sell order at $20.10. River can make more competitive sell offers if she has the ability to rapidly pull them from the market. If Wash has the ability to pounce on River's orders after the market moves, she will need to be more conservative, perhaps offering only $20.15 even though she would be happy to sell at $20.10 (that way she only loses $0.05 if Wash pounces).

### Why does everyone pile on at the same price?

The astute reader will probably ask this straightforward question - why did Mal and Jayne both agree that the best price to offer was $20.07? Isn't it possible that Jayne's calculations predicted the right price to be $20.075, while Mal thought it was $20.071? The answer is yes, it's quite possible that Mal and Jayne actually disagreed on the best price to offer. There is no reason whatsoever why Mal and Jayne's computer programs or trading strategies would both predict prices identical to within many decimal places.

However, regardless of what their trading strategies say, they are not permitted to place orders at their best prices. The [SEC Rule 612](http://www.sec.gov/divisions/marketreg/subpenny612faq.htm) explicitly forbids offering to buy or sell securities in subpenny increments - i.e., `Buy 100 shares @ $20.07` is legal, while `Buy 100 shares @ $20.075` is not. This is also called the Sub-Penny Rule. Prior to 2001, the limit was actually $1/16 or $0.0625.

In real markets, with more than just 4-5 participants, you can also expect many orders to be placed below the top of the book (the highest bid price), at $20.06, $20.05, etc. But the phenomenon of many people piling up near the top of the book does repeat in real life.

## More to come

In this post I discussed the basic mechanics of HFT. In [part 2](/blog/2012/hft_apology2.html) I discuss the social utility and cost, and in [part 3](hft_whats_broken.html) I discuss what's broken and how to fix it.
