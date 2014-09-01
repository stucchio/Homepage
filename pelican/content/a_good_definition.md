title: A good definition is immediately followed by a good theorem
date: 2014-09-02 00:00
author: Chris Stucchio
tags: culture, reasoning, mathematics
mathjax: true
category: culture

> A good definition is 'justified' by the theorem that can be proved with it, just as the proof of the 'theorem' is 'justified' by appealing to a previously given definition.

This quote is attributed to the mathematician [G.C. Rota](http://en.wikipedia.org/wiki/Gian-Carlo_Rota). Last week I wrote an article criticizing the [microservices](|filename|/microservices_for_the_grumpy_neckbeard.md) movement. Of course, nothing I said about microservices was unique to microservices - I could equally well have been writing about full scale Service Oriented Architectures.

The best way to explain the context of the quote in mathematics is by giving a few examples. I promise that this blog post will be fairly elementary - if any mathematical details are difficult to understand, please feel free to skip them. Don't be scared away by the word "Theorem" in bold letters.

# Hausdorff spaces - an appeal to topology

Topology is the study of weird objects together with ways of grouping those objects together. One concept which is important is topology is the notion of "separation".

**Definition:** A topological space is [Hausdorff](http://en.wikipedia.org/wiki/Hausdorff_space) separable if any two distinct points $@ x \neq y $@ can be separated by two open sets $@ U, V $@ with $@ x \in U$@, $@ y \in V $@ and $@ U \cap V = \emptyset $@.

For example, if the topological space consists of the real numbers, then open sets consist of intervals of the form $@ (a,b) $@ (i.e., all numbers greater than but not equal to a, and less then but not equal to b). Any two points $@ x \neq y $@ can be separated with intervals of the form $@ U= (x - 1, 0.5x+0.5y) $@ and $@ V = (0.5x + 0.5y, y+1) $@ (assuming $@ x < y $@).

**Definition:** A sequence $@ x_n $@ in a topological space is [convergent]((http://en.wikipedia.org/wiki/Limit_of_a_sequence#Topological_spaces)) to a point $@ x $@ if for any set $@ U $@ with $@ x \in U$@, we can find some $@ N $@ so that for $@ n > N$@, $@ x_n \in U $@.

As an example of a convergent sequence, think of $@ x_n=1/n $@ and $@ x = 0 $@ - for sufficiently large $@ N $@, any open set containing $@ 0 $@ will also contain $@ x_n $@. I.e., if $@ U = (-10^{-6},10^{-6}) $@, then for $@ N = 10^7 $@, $@ x_n \in U $@.

**Theorem:** Let $@ x_n $@ be a convergent sequence (in the topological sense) in a Hausdorff space. Then the point the sequence converges to is unique.

Hausdorff is a good definition for two important reasons. The first is that it clearly expresses a useful concept - the idea that points can be separated from each other. Not all topological spaces are Hausdorff - the [bug-eyed line](http://en.wikipedia.org/wiki/Non-Hausdorff_manifold) is a good example. The bug-eyed line can be viewed intuitively as the real line, but with both a "red" and "blue" copy of the number zero. On the bug-eyed line, the sequence $@ x_n=1/n $@ has *two limits*: red zero and blue zero. The second is that it is as general as possible - you can construct more restrictive definitions (for example a [metric space](http://en.wikipedia.org/wiki/Metric_space)), but you only need Hausdorff for many theorems to be true. So a good definition embodies only the things that are truly important.

# Without good theorems, the definition doesn't matter

Consider a definition, which you've probably .

**Definition:** A number is fizzbuzz if `n % 3 == 0` and `n % 5 == 0`.

Apart from stupid job interview puzzles, this definition is more or less useless. There are no useful theorems about fizzbuzz numbers. All I've done is assigned a label to a set of numbers. I could equally well define a "blub number" to be a number that either ends in 7 or is divisible by 9. I could make up silly definitions until the cows come home.

But the point of definitions is not merely to label everything - the point of definitions is to label a set of objects which are conceptually different from other objects.

Make no mistake - I can come up with some stupid theorems about fizzbuzz numbers. For example:

**Theorem:** Any non-zero fizzbuss number is not prime.

True as it is, that's a boring theorem. It's boring because it doesn't really help us understand the world. The reason it's boring is because the "fizzbuzz" definition is boring - there are lots of non-fizzbuzz numbers which are not prime. There are very few properties (besides the ones in the definition) which are true of fizzbuzz numbers that are not also true of lots of non-fizzbuzz numbers.

In contrast, consider Hausdorff spaces. Once you give up the Hausdorff property you immediately lose the property of uniqueness of limits.

## Microservices are a bad definition

In my post last week on [microservices](|filename|/microservices_for_the_grumpy_neckbeard.md), I constructed a definition of microservices:

**Definition:** A microservice has no more than 5,000 lines of code and is exposed via a json-over-http protocol which has at most 5 endpoints.

I then "proved" the following "theorem":

**Theorem:** Microservices will make you sad, since they are less reliable and have higher latency than service objects.

"Proved the theorem" is an exaggeration - in reality I used careful reasoning and some simple math to suggest that most of the time, it would be better to use service objects than microservices. I'm using the mathematical language somewhat suggestively, but it should not be taken literally. My "theorem" about microservices is not a real mathematical theorem that is always true - I'm not attempting to assert that it's anything other than a careful argument.

I assert that my blog post from last week was based on a stupid definition. Here's why.

1. If the service were a "macroservice", with 10,000 lines of code and a json-over-http protocol, everything I said would still be true.
2. If the service had 6 json-over-http endpoints, everything I said would still be true.
3. If the service were thrift-over-TFramedTransport (a custom thrift network protocol), everything I said would still be true.

Clearly my definition is insufficiently broad since the conclusion applies to a lot more than just a microservice.

We can improve things by making a better definition:

**Theorem:** Network based services will make you sad, since they are less reliable and have higher latency than service objects.

This is a useful "theorem" because it is based on a good definition. There is a fundamental difference between networked services and in-proc services - the network is orders of magnitude slower and less reliable than simple method calls. Everything else in my definition of microservices is secondary and tangential to the main point.

Until someone comes up with a careful definition of microservice, and comes up with "theorems" that are true for microservices but false for other architectures, I assert that "microservices" is a useless definition. We should completely stop thinking about microservices, and instead focus on what really matters. For example, "should we hide team X behind a rigid API?" "Should the API for team X expose itself via the network or via an interface/trait/abstract class?" "Should team X restrict themselves to < 5,000 lines of code?"

These are the core questions. If we tie ourselves to the definition "microservices" vs "not microservices", we are artificially conflating unrelated issues.

# A bad definition can bias the mind

I assert now that we should be extremely careful with labels. By assigning a label to a concept, the human mind is primed to look for patterns associated to that label. For example, consider the category of "people with type O blood". In Japan, some people believe that people with type O blood are agreeable and sociable. This is a purely artificial pattern which has nothing whatsoever to do with antigen patterns relating to blood compatibility.

The human mind is a pattern matching machine. Creating a definition is a great way to induce the mind to form patterns, whether they are real or not. As a result, I argue that we should all be considerably more careful when we create definitions.

It's also worth being wary of an argument with a high ratio of definition to theorem. It's likely an attempt at making an argument seem solid and carefully thought out, without actually following through on the reasoning. The bias described above is very real, and many people exploit it [as a rhetorical trick](http://squid314.livejournal.com/324594.html).


**See also:** Lesswrong has discussed this concept a bit in the past, for example [Empty Labels](http://lesswrong.com/lw/ns/empty_labels/), the [Consequences of Categorizing](http://lesswrong.com/lw/nx/categorizing_has_consequences/) and [Fallacies of Compression](http://lesswrong.com/lw/nw/fallacies_of_compression/). Scott Alexander describes a rhetorical technique, the [give it a name maneuver](http://squid314.livejournal.com/324594.html) as a way to exploit meaningless definitions in argument. The article [Disputing Definitions](http://lesswrong.com/lw/np/disputing_definitions/) is tangentially related, as is Scott Alexander's [Eighth meditation on Superweapons and Bingo](http://squid314.livejournal.com/329561.html).
