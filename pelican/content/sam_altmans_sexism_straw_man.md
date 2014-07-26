title: Sam Altman's Sexism Straw Man
date: 2014-07-28 00:00
author: Chris Stucchio
tags: culture, probability
category: culture

Sam Altman recently wrote an article about [sexism in technology](http://blog.ycombinator.com/diversity-and-startups). And while I don't dispute many of his factual claims, it's important to recognize the claims he didn't make, and to recognize that most of the article is merely attacking a straw man. Unfortunately, logical fallacy, emotional reasoning and argument by juxtoposition are far too common in discussions of this topic.

The first two sentences of the article set up the straw man:

> Sexism in tech is real.  One of the most insidious things happening in the debate is people claiming versions of "other industries may have problems with sexism, but our industry doesn’t."

It continues:

> Debating how to fix it is important, but debating whether or not sexism actually exists...Saying “There isn’t any sexism in tech” in the face of a mountain of data hurts things in subtle and not-so-subtle ways.

Sam Altman then juxtaposes a discussion of the representation of women in YC:

> We can get more precise number when we disregard background and just look at the gender of applicants (based on looking at the application videos)—19.5% of the startups we have funded this year have women on the founding team compared to approximately 24.3% of startups that applied...

Now it's very important to point out what Sam Altman didn't do. He made *no argument whatsoever* linking the former fact (sexism exists) with the latter fact (women are underrepresented). This is far too common in articles on this topic.

# The real arguments

Now I doubt Sam Altman or other VC types will address this topic logically. It's far easier to send a few token signals and try to fly under the radar than it is to fight against the internet bullies. Rhetorically, the bullies have all the power - accusations of sexism spur an emotional reaction, and arguing against it logically doesn't counter the emotion. But readers of my blog are a select group - if articles like [Asymptotics of Evan Miller's Bayesian A/B Formula](http://chrisstucchio.com/blog/2014/bayesian_asymptotics.html) don't drive them away, pointing out a few bad verbal arguments won't either.

So here are the real arguments which Sam Altman ignored, and will likely suppress on Hacker News (based on the tail end of his article).

## Hypothesis 1: Sexism is not a major problem

It's easy to prove the existence of sexism in technology. It's also easy to prove the existence of murder (google Hans Reiser), theft (laptops have been stolen at tech conferences), and similar things. It's even easy to prove the existence of bias against people without glasses - I recently had LASIK done and since then westerners assume I'm stupid. (This latter bias is primarily a western thing - I've never observed this bias in Indians or Africans.)

Proving that it is a significant factor (for some definition of "significant") is harder. You can't simply cite the "lived experience" of a few activists. To prove it is a significant factor, you need data. Sam Altman provides no data, no argument, nothing.

## Hypothesis 2: Sexism does not cause the underrepresentation of women

Sam Altman attempts to argue against this by juxtuposition. He first discusses the existence of sexism, and second discusses underrepresentation of women. The reader might emotionally believe they are connected, but Altman provides no argument connecting them. He then attempts to dismiss one of the arguments in favor of Hypothesis 2, but his anecodote actually supports it:

> I’m willing to believe it’s worse in other industries [1], but it’s still very bad in our own industry...[1] My mom is a doctor...My mom pointed out to me there was a men’s bathroom but no women’s bathroom.

So here is the *logical argument* in favor of Hypothesis 2. Other industries such as medicine were *more sexist than tech currently is*. Women entered those industries and achieved equal representation. This suggests that there isn't even a strong correlation between sexism in an industry and women's representation there.

Or consider an organization which *strictly forbids* women from taking the primary leadership role. The guiding document of that organization considers women subservient to men, claims wives must obey their husbands, and is generally medieval in it's outlook. (This organization is also generally opposed to homosexuality.) The Catholic Church has a diversity problem - it has [too few men](http://www.jsonline.com/news/religion/with-leadership-dominated-by-women-churches-reaching-out-to-men-b99135844z1-233951051.html). (Hat tip: [Scott Alexander](http://slatestarcodex.com/2014/01/12/a-response-to-apophemi-on-triggers/) )

# Sexism is real and Altman's numbers suggest YC suffers from it

A mathematical exercise. Suppose you have a selection process. You want to measure a quality score Q. But your actual measurement M does not measure Q only - it also has a bias built in. Suppose for a baseline group, M = Q, but for a subgroup, M = Q + B (where B can be positive or negative). What do we predict the outcome will be?

Now suppose you allow in applicants provided M > C. How can you measure B? The answer is to look at outcomes, which are presumably correlated to Q. Simply rearranging the numbers shows the effect of bias on outcomes:

    Outcome = M - B

So if bias is negative (women are discriminated against), outcomes will be higher for YC startups with women than without. If bias is positive, you'll find that outcomes are lower for women. Altman *almost* provides data on this - if you compare his 20% of YC is female to 10% of top companies are run by women, you observe a bias in favor of women. However, the 10% number actually represents companies where women are the CEO, while the 20% number represents teams containing women.

If Altman reveals the number of companies worth more than $100M with women on the founding team, we can get an estimate of whether YC is really biased.

(Note: I realize that in real life things are noisy. That doesn't change the reasoning here, it merely makes it harder to measure.)

# Conclusion

The topic of too many white/asian males in computing is a popular topic, and generally one worth ignoring. The quality of the discussion is low, most people get emotional about it, [rhetorical superweapons](http://slatestarcodex.com/2014/05/12/weak-men-are-superweapons/) are built and used, and one learns nothing by reading these discussions.

Also, full disclosure. I am a White/Asian Male (TM) attempting to maintain my superiority. I hate non-Asian minorities and women so much that I moved to location which is almost exclusively full of [white/asians](http://en.wikipedia.org/wiki/Demographics_of_India) and which also has 1.06 males for every female. Additionally, I'm a neckbeard who can't get laid, I wear a fedora, and I'm generally a low status individual. (Just want to head off all the obvious responses.)
