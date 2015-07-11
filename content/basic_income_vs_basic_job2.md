title: Models help you understand why you disagree
date: 2013-11-14 08:00
author: Chris Stucchio
tags: statistics, public policy, economics, monte carlo





In a [blog post yesterday](/blog/2013/basic_income_vs_basic_job.html), I advocated very strongly that rather than simply bloviating about political (and other) topics, we should instead build mathematical models to clearly express our thinking. There was a [lot of disagreement](https://news.ycombinator.com/item?id=6725096) on this. But quite a few people took the point to heart, and several actually decided to modify my model to illustrate their thinking. One in particular was [Jeremy Scheff](http://www.jeremyscheff.com/2013/11/basic-income-vs-basic-job/), who who [forked my model](https://gist.github.com/jdscheff/7457890) and came up with his own. His model has a very different answer.

I'm going to briefly address his model to demonstrate how models help us have a rational discussion.




Jeremy alters my model in several ways. His first tweak is to cut the direct costs of a Basic Income in half:

> In Chris's model, basic income is paid to everyone. It is also possible to have a system like progressive income tax, where it gradually phases out; in fact, fellow Rutgers alumnus Milton Friedman proposed to implement basic income through a negative income tax. So let's imagine some system like that and reduce the costs by 50% right off the bat.

He is very explicit about this. I copied this change over from his model to mine, and it has a dramatic effect - the cost of the Basic Income is in fact cut from about $3 trillion to $1.5 trillion when you do this.

This is a major point of disagreement between us. He believes this a realistic change that can be made, but I simply don't understand it. This is part of the reason we disagree. A major step towards the two of us agreeing with each other would be to evaluate this proposition - can it possibly work his way? If so, how? Is there data we can dig up to figure this out one way or the other?

A second place where his model disagrees with mine is that he believes a largeish number of people are not really disabled, and a Basic Income would induce them to engage in productive work:

> At this point, I want to add an effect that has been neglected. Chris treated the number of disabled adults as a constant, but that is [likely not true](http://apps.npr.org/unfit-for-work/). So let's conservatively say 2 million people currently on disability would start working if they got a basic income, likely at some not-so-great wage.

He includes a to account for this effect. I copied this term only over to my model, and reran it. It didn't change much of anything. This is also good to know. If Jeremy and I were bloviating on /r/politics, we could spend hours debating whether this effect is real or not. Because we have a model to work from, we now know that this effect simply doesn't matter much and won't spend much time debating it.

A third effect he thought of that I didn't is a productivity multiplier - essentially, he believes that a Basic Income might make working adults up to 20% more productive. I'm not convinced by this at all, but at least I understand what he thinks would happen. I copied this change only over to my model, and it also turns out to have a big effect. This is another point that is worth discussing.

The final place where we disagree is that he believes it to be quite possible that the people working basic jobs will actually be destructive - perhaps they buy into the [Broken Window fallacy](https://en.wikipedia.org/wiki/Parable_of_the_broken_window):

> Chris says it's worth somewhere between $0/hr and $7.25/hr, as otherwise they'd probably be working a minimum wage or higher job. Sounds reasonable enough, but there are also people who bring negative value to the table. These people would be forced to work, likely in some boring job they hate.

Altering this assumption might make the Basic Job up to $500B more expensive. It's not a small number, but it's not that big an issue either.

Jeremy was very [explicit](https://gist.github.com/jdscheff/7457890/revisions) about what he disagreed with me on. His explicitness allowed me to go diff by diff and figure out why we really disagree, and which disagreements actually matter. Now we can move forward. The main things we need to figure out are whether his alternate implementation of BI can cut the direct costs in half, and whether BI can really add 20% to worker productivity.

Presumably, treating us both as rational actors, once we find data to address these points, we will update our beliefs and come to agreement. And that's why models are important. They aren't magic oracles to tell us the answer, they are simply communication devices to make our thinking clear and calculation devices to prevent us from making logical errors (e.g. thinking that the `undisabled_cost_benefit` or that `jk_rowling()` will change the result).

Incidentally, I'm not really planning to try to change Jeremy's mind here because there is very little data to actually address the points where we disagree. I'm also scared of becoming a political blogger - among other things, the commenters on those blogs are all a bunch of idiots and I'm happy not to have them as readers. The ideology I'm pushing here is [epistemiological](https://en.wikipedia.org/wiki/Epistemology), not political. I have a far stronger desire to convert my readers into Bayesians than I do to convert them to my niche brand of capitalistic liberalism.
