title: Book reviews - stuck in the hospital edition
date: 2014-10-27 09:00
author: Chris Stucchio
tags: data science, mathematics,
nolinkback: true
category: book review

![into hospital](|filename|/blog_media/2014/data_science_foundations_and_others_review/into_hospital.jpg)

The last month or so of my life hasn't been awesome. That's me prepped for surgery. But life is improving - I'm now out of the hospital, with both the upper and lower half of my body pain free! While I was inside, I had a lot of time to read - as a result, here come some book reviews.

# **Go read right now:** Foundations of Data Science, by John Hopcroft and Ravindran Kannan

Summary: [Go read this book now](http://www.cs.cornell.edu/jeh/NOSOLUTIONS90413.pdf).

Data science tends to consist of two somewhat disparate parts. On the one hand, there are a variety of practical algorithms, together with various tricks for implementing them, which can be used more or less as black box learning tools. Most of the textbooks I've seen focus on describing these algorithms, while providing enough theory to get to the point where they can be explained. On the other hand, there is quite a bit of mathematical theory and intuition, which most books don't provide a great deal of explanation for.

As a concrete example, consider a higher dimensional vector space - a set of points `x = [x1, x2, ..., xn]` for `n=100` or `n=1000`. Now suppose such a set of points is drawn from a gaussian mixture - say `w1*N(m1,sigma1) +w2*N(m2,sigma2)`. Most textbooks will give you a variety of algorithms you can implement in code for estimating `w1, w2, m1, m2, sigma1, sigma2`. They may provide a proof that the algorithm will converge, that it will nicely separate the two gaussians, and so on. However, in my opinion, most such books fail at giving good intuition about the geometry of 1000-dimensional space. As a result, they fail to provide a good understanding of why these algorithms actually work.

There are a LOT of books which fall into this category.

Foundations of Data Science (henceforth FODS) is different. The first chapter of FODS covers high dimensional geometry in a rigorous and intuitive manner. Rather than giving you an algorithm to implement, FODS explains the key properties that enable you to separate gaussian mixtures. For example, the diameter of the unit cube in N-dimensions grows like `O(sqrt(N))` - by comparison, the diameter of the unit sphere is `O(1)`. Similarly, the volume of the unit cube is located near the corners, the volume of the unit sphere is located near the surface, and so on. These are important geometric facts which underlie virtually every vector space method in machine learning. Building up knowledge and intuition of this sort is the focus of FODS.

So far, FODS is the ONLY book I've seen that falls into this category. As such, for anyone who wishes to learn data science, I strongly recommend reading FODS together with any other book.

The first two chapters alone (which cover high dimensional vector spaces and singular value decompositions) make FODS well worth reading. The book also covers random graphs, markov chains, and much later on in the book actually teaches some algorithms. I didn't actually get that far during my hospital stay, so I can't say every chapter is perfect. But overall, it's a fantastic book.

Did I mention that [it's available for free](http://research.microsoft.com/en-us/people/navingo/e0-229.aspx)? Go read it now.

# **Skip:** Antifragile, by Nassim Taleb

Summary: You'll feel smart but you won't learn anything.

Before reading this book, my feelings about Nassim Taleb were mixed. On various occasions I've read statistical papers he's written. These papers tend to be carefully written, on-point, well supported, and generally well worth reading. Their focus is narrow - e.g., given a variable asymptotically distributed like `x^{-alpha}`, what biases are inherent in measuring `alpha`? There are many charlatans who spout platitudes while being ignorant of the technical details. Taleb is definitely not one of them.

On the other hand, I've also read articles by Talbe writtenfor a popular audience, and I've found it to be content-free New Yorker style prattle. A perfect example is this [execrable article]() about why Standard Deviations are evil and should never be used. It makes you feel smart when you read it - Taleb exudes intelligence, contrarianism, and disdain for the nerds who actually handle the technicalities. When writing for a popular audience, Taleb lets you feel smart without actually having to exercise your brain.

Antifragile falls solidly into the latter category. Taleb's main thesis is that some things in the world are "antifragile", which means that after subjecting them to certain types of "randomness", they "improve". What this means in general is pretty vague. But Taleb lifts weights, so bones are antifragile. Isn't he awesome? Regulators trying to ensure stability are fragile, but the free market system where companies go bankrupt regularly is antifragile. Unlike those nerdy regulators, Taleb has good intuition and a nose for bullshit. You too, dear reader, are smart - look at how easy it would be to apply hindsight to stop the financial crisis!

I don't particularly disagree with most of Taleb's isolated claims. I also lift (or at least I did until my disks stopped being antifragile), I hate regulators, and generally oppose attempts to control and stabilize things. Yay, Taleb is just like me! But he doesn't really make any good arguments that antifragile is a real thing. The book is just smug verbosity and flattery towards the reader. Those are both perfectly fine things to have, but you need to put some substance behind it.

If you want to feel smarter without actually becoming smarter, go buy [Antifragile](http://www.amazon.com/gp/product/0812979680/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=0812979680&linkCode=as2&tag=christuc-20&linkId=PSPH6MWDWJRWLSSZ).

# **Skip:** Flash Boys, by Michael Lewis

Summary: If you don't already know how HFT works, you'll find yourself dumber than before you read the book.

I finally got around to finishing this book. It's a wonderful study in how one can carefully use language, tone, implication and anecdote to create the illusion of a strong argument. I've discussed the detailed allegations of Michael Lewis' claims in other blog posts:

[A fervent Defense of Front Running HFT's](|filename|fervent_defense_of_frontrunning_hfts.md)
[Mark Cuban's HFT Idiocy](|filename|mark_cubans_hft_idiocy.md)

What I found remarkable when reading the book is how content-free the book is. The key allegation made in the book is that market makers [price discriminate](|filename|fervent_defense_of_frontrunning_hfts.md) against informed traders (e.g. Goldman Sachds) and in favor of the little guy (Joe 401k). Most of the rest of the book is just vague description of various order routing technologies, together with language carefully designed to make the reader feel in their gut that something nefarious is happening.

For example, Lewis discusses how those evil HFT's pay for order flow. This is another mechanism by which HFT's price discriminate - they offer good prices in internal dark pools to fill retail orders (read: Joe 401k), while offering worse prices in the public exchanges (where big informed players lurk). Lewis describes this as "picking off" the slow retail traders who are "seconds behind". The idea of placing an order on eTrade and then getting a fill sure sounds nefarious when phrased this way. Somehow Lewis spins this as not being in the interest of the retail trader.

Dark pools are also briefly mentioned, and they too are evil scary things which eliminate transparency. Except of course for IEX which Lewis somehow manages to describe as an "exchange" for most of the book. (It's a dark pool.) The noble goals of the IEX founders also get a lot of discussion.

The interesting thing to look for in this book is the use of language and implication. Lewis uses terms like "picking off", "front run", and similar a lot, but it's rarely clear what the words mean. Sometimes it means filling other people's orders, sometimes it means cancelling orders. Sometimes being the fastest HFT and getting to the top of the queue with a limit order is "front running", sometimes being slower but using a better strategy (Hide-Not-Slide orders) is. The only consistent thing is that if the term sounds negative, it means "whatever the HFT's are doing this chapter". If it sounds positive, it describes whatever IEX is doing.

If you want to learn the actual mechanics of HFT, go read my [introduction](|filename|hft_apology.md), [introduction part 2](|filename|hft_apology2.md) and [part 3](|filename|hft_whats_broken.md). Unfortunately, the actual mechanics of how a matching engine or dark pool works are not included in this 288 page tome.

If you want to pay $15 for an IEX advertisement, [go read Flash Boys](http://www.amazon.com/gp/product/0393244660/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=0393244660&linkCode=as2&tag=christuc-20&linkId=E4GL3CAMJSCHCMLD). You can also follow IEX [on facebook](https://facebook.com/iamaninvestor), [join the movement](http://www.iextrading.com/insight/letter/) to persuade your broker to use IEX, andprobably lots more social media type stuff. I'm really not joking.

(In case you were wondering, IEX is having a bit of difficulty supplying liquidity to their customers without HFTs. Their strategy seems to be replacing smart market makers with dumb retail flow in their dark pool in order to attract liquidity from the big boys.)

Disclaimer: I used to be an HFT. Now I'm a daytrader who is happy when HFT's "pick me off".
