Why you can't have privacy on the internet
##########################################
:date: 2018-08-09 08:30
:author: Chris Stucchio
:tags: economics, privacy


I recently attended a discussion at `Fifth Elephant <https://fifthelephant.in/>`_ on privacy. During the panel, one of the panelists asked the audience: "how many of you are concerned about your privacy online, and take steps to protect it?"

At this point, most of the hands in the panel shot up.

After that, I decided to ask the naughty question: "how many of you pay at least 500rs/month for services that give you privacy?"

Very few hands shot up.

Let me emphasize that this was a self selected group, a set of people at a technology conference who were so interested in privacy that they chose to attend a panel discussion on it (instead of concurrent talks on object detection and explainable algorithms). Besides me and perhaps 2 or 3 others, no one was willing to pay for privacy.

Instead of paying for it, many of the people at the panel wanted the government to mandate it. Moreover, many people seemed to think it would somehow be free to provide.

People won't pay for privacy
============================

Online Services Aren't Free
---------------------------

    If you are not paying for it, you're not the customer; you're the product being sold.

Every online service costs money to provide. To get an idea on the metrics, here are some `leaked revenues at a company I worked for <https://techcrunch.com/2013/08/18/inside-patchs-leaked-revenue-numbers-and-its-hunt-for-profitability/>`_. Content isn't free. Engineers aren't free. Ad revenues aren't very high. If the site is storing lots of personal data (e.g. email, picture/videos, etc), even the cost of computing infrastructure can become significant.

Since most people are unwilling to pay for online services, the way to cover these costs is by advertising to the users.

**Ad revenue per user varies by several orders of magnitude depending on how well targeted it is.**

Here's a calculation, which was originally done by `Patrick McKenzie <https://twitter.com/patio11/status/875629380105416705>`_ to answer the question


    I just bought a refrigerator yesterday. Why, why, why do you show me refrigerator ads?


1. Assume a typical person buys a refrigerator once every 10 years.
2. Assume 2% of refrigerator purchases go wrong (e.g. your wife hates it, it breaks), and you need to buy a new refrigerator within a week.

Subject to these assumptions, a person who's bought a refrigerator is 10x more likely to buy another refrigerator in the next week than someone who hasn't.

The fundamental problem of advertising is sparsity - the fact that most advertisements are worthless to most people. An ad for "faster than FFTW" might be useful to me, but it's pointless for most people who've never heard of FFTW. If you haven't spied on me well enough to know that I do fast fourier transforms, your odds of making money by advertising to me are essentially zero.

Advertising generates negligible revenue without personalization.

Without advertising, people will need to pay for their online services. Email services tend to cost around $5-10/month. The NY Times costs about $10/month, and the Wall St. Journal costs 2-4x that. It's hard to guesstimate the cost of social networks, but my best guesstimates for Facebook is several dollars per user per month.

**Will you pay $20-50 a month to replace your free online services with privacy preserving ones?**

Another major fact is that service providers use data to improve their service. User tracking enables product managers/UI designers to figure out exactly what customers want, and give it to them. Google cannot index your email and make it searcheable without also reading it. **Would you use a free email product with a much worse UI than Gmail?**

Fraud is real and pervasive
---------------------------

Consider your payment provider - PayPal, PayTM, Simpl (disclaimer: I work there), etc. One of the most invisible and pervasive concerns at a company like this is preventing fraud.

The economics of a payment provider are as follows:

1. A customer books a 100rs movie ticket on BookMyShow.
2. The customer pays 100rs to the payment provider.
3. The payment provider transfers 97-99.5rs to BookMyShow and pays for their expenses with the remaining 0.5-3rs.

That's a pretty tight margin. For concreteness and simplicity of exposition, lets suppose the `Merchant Discount Rate <https://www.investopedia.com/terms/m/merchant-discount-rate.asp>`_ is 1%.

Now lets consider the impact of fraud. If fraud levels ever get as high as 1 transaction out of every 100, the payment provider will have zero revenue and will go broke. If fraud is not carefully controlled, it can reach levels far higher than this.

    In mid-2000, we had survived the dot-com crash and we were growing fast, but we faced one huge problem: we were losing upwards of $10 million to credit card fraud every month.

-- `Peter Thiel, Zero to One <https://amzn.to/2vCKssB>`_

Peter Thiel notes that reducing fraud was the difference between loss and profitability.

In the long run, the cost of fraud must be passed on to the consumer. Either the payment provider or the merchant will eat the cost of fraud, and will in turn raise prices on consumers to compensate.

**Will you pay 120rs for a 100rs movie ticket in order to protect your privacy from your payment provider?** It's important to note that while the extra 20rs may seem to go to the payment network in reality it will go to the smartest scammers.

There is plenty of fraud that occurs beyond payment networks. On Uber, there are fake drivers that take fake passengers on trips and demand to be paid even though the fake passengers have paid with stolen credit cards. Many fraud rings attempt to misuse incentive systems (e.g. "refer a friend, get 100rs off your next order") in order to generate credits with which they can purchase saleable goods. A merchant aggregator is also at risk from the submerchants; movie theatres/restaurants/etc will attempt to exploit BookMyShow/Seamless/etc, in general, submerchants will attempt to make fraudulent transactions on the aggregator and demand payment for them.

A special case of fraud which also relates to the problem of paying for services with advertising is display network fraud. Here's how it works. I run "My Cool Awesome Website About Celebrities", and engage in all the trappings of a legitimate website - creating content, hiring editors, etc. Then I pay some kids in Ukraine to build bots that browse the site and click the ads. Instant money, at the expense of the advertisers. To prevent this, the ad network demands the ability to spy on users in order to distinguish between bots and humans.

Even if you were willing to pay for it, privacy is illegal
==========================================================

**Question**: What does the government call a payment platform that provides privacy to it's users?

**Answer**: Money laundering.

Here in India, the bulk of the privacy intrusions I run into are coming from the government. It is government regulations which require me to submit passport photocopies/personal references/etcto get a SIM card, government regulations requiring an OTP in order to use free Wifi at Starbucks (thus connecting my internet usage to said SIM), and prohibitions against the use of encryption are generally pushed by national governments. Things were pretty similar in the US.

It is, of course, impossible for a service provider to satisfy the government's desire to spy on users without doing so itself.

The desire for the government to spy on users extends far beyond preventing money laundering. In the United States, Congress has demanded information and action from technology companies in order to prevent Russians from posting Pepe memes on Twitter or attempting to organize "Blacktivism" on Facebook. The Kingdom bans most encrypted communication, and many democratic nations (the US, India,

In the intermediary stages, there is a large amount of information that the government requires service providers to keep. This typically includes accounting details (required by tax departments), both purchase history as well as KYC information used by tax authorities to track down tax evaders (e.g., Amazon is required to keep and provide to the IRS tax related information about vendors using Amazon as a platform).

In many cases, censorship authorities require social networks and others to track and notify them about people posting illegal content (Nazi imagery, child pornography, Savita Bhabhi, anti-Islamic content).

Fundamentally, it is government regulations that `shut down cryptocurrency exchanges in India <https://qz.com/india/1322393/rbis-bitcoin-ban-how-indian-cryptocurrency-exchanges-are-trying-to-survive/>`_. It is government regulations that `ban encrypted communication in the Kingdom <http://gulfbusiness.com/saudi-lifts-skype-whatsapp-ban-will-censor-calls/>`_ (at least partially), and it was politicians in `the US and UK <https://en.wikipedia.org/wiki/Crypto_war>`_ and `India <https://scroll.in/article/810568/meet-the-man-whos-addicted-to-whatsapp-but-moved-the-supreme-court-to-have-it-banned>`_ who want to move in the same direction.

Insofar as privacy preserving platforms might exist, it is far from clear whether governments will allow them to continue existing should they become popular.

The privacy preserving service has approximately three crypto geeks and seven zillion Ukrainians hackers laundering money on it
===============================================================================================================================

    . . .if you're against witch-hunts, and you promise to found your own little utopian community where witch-hunts will never happen, your new society will end up consisting of approximately three principled civil libertarians and seven zillion witches. It will be a terrible place to live even if witch-hunts are genuinely wrong.

-- `Scott Alexander <http://slatestarcodex.com/2017/05/01/neutral-vs-conservative-the-eternal-struggle/>`_

Unfortunately, this Scott Alexander quote explains very nicely what will happen when someone builds a moderately successful privacy preserving network.

If we built a privacy preserving payment network, it would be used for money laundering, `drug sales <https://en.wikipedia.org/wiki/Silk_Road_(marketplace)>`_ and `ransomware <https://www.wsj.com/articles/in-the-bitcoin-era-ransomware-attacks-surge-1471616632>`_. If the `Brave private browser/micropayment system <https://brave.com/publishers/>`_ ever approaches viability, it will be overrun by criminals laundering money through blogs about Ukrainian food.

If an ad network vowed to protect privacy, fraud would shoot up and good advertisers would leave. The few remaining customers would be selling penis enlargement pills, accepting the click fraud as the cost of doing business because no one else will work with them.

There are privacy preserving/censorship resistant `social <https://voat.co/>`_  `networks <https://gab.ai/>`_. They're full of Nazis.

This is a fundamental collective action problem, and no player in the game seems to have the ability change things. There are bad actors out there - fraudsters/scammers, terrorists laundering money, legal gun manufacturers moving money around, child pornographers, people who believe in evolution (even `among humans <https://hbdchick.wordpress.com/category/what-is-human-biodiversity/>`_), people `advocating abandoning Islam <https://exmuslims.org/>`_, Russians posting Pepe memes, and journalists/revenge pornographers revealing truthful information that people want kept hidden. Any privacy preserving network, at it's core, allows these people to engage in these actions without interference.

And as any network approaches viability, it's early adopters will be these sorts of undesirables.

Make no mistake; I want this privacy preserving network to exist. But the first step in making that happen is recognizing and acknowledging the very real barriers to making it happen.
