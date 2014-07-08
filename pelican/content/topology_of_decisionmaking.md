title: Topology of decisionmaking - are you secretly managing by metric?
date: 2014-07-08 09:00
author: Chris Stucchio
tags: metrics, data analysis, topology, decisionmaking
mathjax: true
summary: Suppose you have a method of making decisions that doesn't suck - i.e., one that is objective, consistent, and never leaves you guessing about what to do. The mathematical field of topology provides a wonderful theorem - if you have a good decision process, it is equivalent to managing by metric.

Humans generally take two different approaches to rational decisionmaking. The first approach is *management by metric* which involves reducing each choice to a single number and then choosing whichever choice has the larger number. In education, this involves assigning a student a score based on performance on a set of exams - this score can then be compared to a fixed performance standard to determine whether a student passed or failed. In trading, management by metric involves evaluating a trader based on [Sharpe ratios](http://en.wikipedia.org/wiki/Sharpe_ratio), [alpha](http://en.wikipedia.org/wiki/Alpha_(investment)) generated above a benchmark, and similar measures.

The competing method, which I *holistic*, involves humans accounting for all features of the choices and emitting a decision on the basis of careful consideration. In trading, it would involve senior managers forming opinions about traders and evaluating them on that basis. In education, it might involve a teacher giving an oral exam to a student, letting the conversation flow, and then evaluating whether they seem to discuss issues at a 5'th grade level. I use holistic as a catch-all term to describe anything besides management by metric.

Are these two decisionmaking techniques significantly different? In this blog post I'll use topology to show that the answer is no - if your decision process doesn't suck, then it's equivalent to managing by metric for some specific metric.

I'll begin by describing the properties that any good decision process should satisfy.

# Properties of a good decision process

To begin with let us define some notation. Consider two elements of our set of choices, $@ x $@ and $@ y $@. We will write

$$ x \leq y $$

if our decision process says the choice $@ y $@ is not inferior to $@ x $@. We will write

$$ x \sim y $$

whenever both $@ x \leq y $@ and $@ y \leq x $@. The property $@ x \sim y $@ means we can choose $@ x $@ or $@ y $@ at random - we are indifferent. We also write:

$$ x < y $$

if $@ x \leq y $@ but not $@ x \sim y $@.

## Property 1: Decisiveness (aka totality)

The first property a decision process should have is that it actually makes a decision. I.e., for every possible choice $@ x $@ and $@ y $@, either

$$ x \leq y \textrm{ or } y \leq x .$$

It's important to note what happens if we do not have decisiveness. In this case, *we fail to make a decision*. This is not the same thing as declaring $@ x \sim y $@ - in that case, we choose one arbitrarily and move on. A lack of decisiveness means that in a very strict sense, your decision process fails to make a choice. In computational terms (assuming the decision is made by computer) this means your computer hangs forever, segfaults, emits $@ \bot $@ or otherwise engages in undefined behavior.

**Note:** This does not mean the decision process can always determine the best choice. It merely means that it can make *some* choice.

## Property 2: Consistency (aka transitivity)

The second important property a decision process should have is consistency. This means:

$$ \textrm{ if } x \leq y \textrm{ and } y \leq z \textrm { then } x \leq z $$

In mathematics this property is called transitivity.

The property of consistency/transitivity is very important when you have more than two choices - without the property of transitivity, it is impossible to deterministically compute a maximal element of a finite set.

**Definition:** The maximal element of a set $@ S $@ is an element $@ m \in S $@ with the property that for every $@ s \in S$@, $@ m \geq s $@.

If we must make a choice between all the elements of $@ S $@, the maximal element is the one we would choose.

### Why we need consistency

Consider now a set of elements which break transitivity. Suppose we have $@ a < b$@, $@ b < c$@ and $@ c < a $@. No matter which element in the set we choose, we can always find another one which is superior. The set $@ \\{a, b, c \\} $@ *has no maximal element*! We have no deterministic method of choosing between these alternatives.

Even when we must make pairwise choices, we can still run into trouble without transitivity. Consider a set of students together with a standard of performance to pass a class. I.e.:

$$ \textrm{Priyanka} \geq \textrm{standard} $$

means that Priyanka will pass the class. Similarly:

$$ \textrm{Sandeep} \geq \textrm{Priyanka} $$

means that Sandeep performed better than Priyanka. But without transitivity, it could happen that

$$ \textrm{standard} \geq \textrm{Sandeep} $$

This is a rather perverse situation - Sandeep performed better than Priyanka, yet Sandeep failed and Priyanka passed.

## Property 3: Objectivity (aka determinism)

Objectivity simply means that your decision process works and gives the same answer regardless of who is running it. This is less a mathematical point and more a computer science point - it means the function computing your decision is [pure](http://en.wikipedia.org/wiki/Pure_function).

In practice, objectivity means that the internal details of the decision process do not change the outcome. For example, consider the process of grading an exam. Given a grading rubric, the process is objective/deterministic; computing an indefinite integral but forgetting the "+ C" term results in a loss of 2 marks, just as the rubric says. It does not matter whether it is graded by me, a teaching assistant, or anyone else - the outcome is the same.

In contrast, if the teaching assistent were more generous than me with partial credit, the process would fail the objectivity property.

### A failure of objectivity

Consider the following holistic decisionmaking process. Two adversaries enter a room and argue in favor of choice $@ x $@ and $@ y $@, respectively. Each one has an incentive to introduce all possible evidence to prove his position. An uninterested and impartial Judge will then make decisions based on this evidence. Yes, this describes the Israeli court system, and court systems in most other nations.

In at least one experiment, this process has been shown to fail the property of objectivity. It turns out that strong variations are introduced into the decisionmaking process [based on how hungry the Judge is](http://blogs.discovermagazine.com/notrocketscience/2011/04/11/justice-is-served-but-more-so-after-lunch-how-food-breaks-sway-the-decisions-of-judges/#.U7bNFnV53UY).

# Consistency in the face of new information

Let us now consider a real world example to understand what these terms mean. We want to hire a single candidate to work as a fetcher - their job will be to run into a warehouse and retrieve items when requested.

At 12:00, the candidates all walk into the room. We see Monika, a 5'2" skinny female, Pandit, a 6'1" skinny male, and Pooja, a 5'4" chubby female. Based on physical appearance alone we mentally construct a ranking:

$$ \textrm{Pandit} > \textrm{Monika} > \textrm{Pooja} $$

This ranking is based on the theory that the tall person can retrieve items from the top shelf quickly (not needing a ladder) and the fat person is more likely than the thin person to be slow and lazy.

Now suppose we subject the candidates to a work sample test - we ask them to retrieve items and time them. Based on this test, we observe that Monika is very good at climbing, and is able to quickly retrieve items from high shelves. The net result:

$$ \textrm{Monika} > \textrm{Pandit} > \textrm{Pooja} $$

As a result, we hire Monika. Have we violated either the consistency or objectivity property?

The answer is no. Our *choice set* represents both the policies we can choose and the information we have about them. Before the work test our choices were:

$$ \\{ (\textrm{tall male}, ?), (\textrm{skinny female}, ?), (\textrm{chubby female}, ?) \\} $$

After the work sample test our choices changed. The old choices (the ones missing information) are gone forever, and the new choices are:

$$ \\{ (\textrm{tall male}, \textrm{medium speed}), (\textrm{skinny female}, \textrm{fast}), (\textrm{chubby female}, \textrm{slow}) \\} $$

So our *decision process* has remained constant in light of new information - it's the *choice set* which has changed.

None of the properties described above preclude changing one's mind based on new information - they simply preclude changing one's mind for no reason at all.

# Management by metric - Theorems for free!

We define management by metric to be the following decision process. Consider the set of choices $@ X $@. Then there is a metric, i.e. a function $@ d : X \rightarrow \mathbb{R} $@ which reduces each choice to a single number. Whenever

$$ d(x) > d(y) $$

we choose $@ x $@ over $@ y $@. We also assume the function $@ d(x) $@ to be deterministic - it always returns the same answer.

It's not hard to see why management by metric satisfies the 3 properties listed above. It satisfies decisiveness/totality because the standard ordering on the real numbers is total - either $@ a \leq b $@ or $@ b \leq a $@ for any two real numbers.

It satisfies transitivity because if $@ d(x) \leq d(y) $@ and $@ d(y) \leq d(z) $@, then $@ d(x) \leq d(z) $@ - again, this follows from the transitivity of < on the real numbers.

A large part of the appeal of management by metric is all the theorems that come for free. If you actively design your decision process to first compute a metric, then use the metric to make choices, you don't have to worry about accidentally being inconsistent or subjective. Deliberate metric-based decisionmaking gives you all the good properties of a decision process for free.

# Topology

One of the earliest topics studied in topology is the study of orderings. An ordering is a relation like our $@ \leq $@ relation above. There are a variety of types of relations, each satisfying more stringent assumptions.

A preorder is simply a relation which satisfies reflexivity (namely $@ x \leq x $@) and consistency (aka transitivity). A partial order adds the requirement of antisymmetry - if $@ x \leq y $@ and $@ y \leq x $@ then $@ x = y $@. A [total order](http://en.wikipedia.org/wiki/Total_order) is a partial order together with the decisiveness property.

The decision process I'm describing in this post satisfies all the properties of a total order except for antisymmetry.

So here is the fun topological fact.

**Theorem:** Suppose you have a decisive, consistent and objective method of making decisions. Suppose further that the set of decisions is no more than countably infinite. Then there exists a metric $@ d : X \rightarrow \mathbb{R} $@ with the property that:

$$ d(x) > d(y) \textrm{ if and only if } x \geq y $$

In words, this means whenever you have a decisive, consistent and objective decision process, then someone who is managing by metric (for a suitable choice of metric) can make the *exact same decisions*.

I'm writing this as a mathematical proof, but I urge the reader to try and read it. The proof is fairly simple induction/recursion and hopefully should be accessible to anyone with a computer science background.

**Proof:** The goal here is to show that whenever we have a decisive, consistent and objective process, we are managing by metric. To do this, we must build the metric function $@ d(x) $@.

To begin, number the possible choices $@ x_0, x_1, x_2, \ldots $@. Then define:

$$ d(x_0) = 0. $$

Now, for $@ i \geq 1 $@, we define $@ d(x_i) $@ as follows.

1. If $@ x_i > x_j $@ for every $@ j < i $@, then we define $@ d(x_i) = \max_{j < i} d(x_j) + 1 $@.
2. If $@ x_i < \min_{j < i} x_j $@, then we define $@ d(x_i) = \min_{j < i} d(x_j) - 1 $@.
3. If $@ x_i \sim x_j $@ for any $@ j < i $@, then we define $@ d(x_i) = d(x_j)$@.
4. If none of the above conditions are satisfied, then we define:
$$ d(x_i) = \frac{1}{2} \left( \max_{x_j < x_i} d(x_j) + \min_{x_j > x_i} d(x_j) \right)$$

In the last case, we are simply collecting all the items smaller than $@ x_i $@, all the iterms bigger than $@ x_i $@, and assigning $@ d(x_i) $@ to the midoint of the region between those. In pictures:

![rule 4](/blog_media/2014/one_true_metric/rule_4.png)

The x-position of the dots represent the real number line, while the y-positions are meaningless (and all zero). The red dots represent the values $@ d(x_j) $@ for $@ x_j < x_i $@, the blue dots represent the values $@ d(x_j) $@ for $@ x_j > x_i $@, and the green dot represents $@ d(x_i) $@ itself.

We now need to show that if $@ x_j < x_i $@, then $@ d(x_j) < d(x_i) $@. This means that using our decision process is equivalent to managing by metric, for the specific metric $@ d $@.

1. We have that $@ x_i > x_j $@ for every $@ j < i$@. Clearly $@ d(x_i) = \max_{j < i} d(x_j) + 1 > d(x_j) $@.
2. Just flip around the previous case.
3. Suppose $@ x_i \sim x_j $@. Since $@ d(x_i) = d(x_j) $@, then $@ d(x_i) \leq d(x_j) $@ and $@ d(x_i) \geq d(x_j) $@ we are done.
4. For any $@ x_j \leq x_i $@, we have:

$$ d(x_i) = \frac{1}{2} \left( \max_{x_j < x_i} d(x_j) + \min_{x_j > x_i} d(x_j) \right) \geq \frac{1}{2} \left( \max_{x_j < x_i} d(x_j) + \max_{x_j < x_i} d(x_j) \right)$$
$$ \geq \left( \max_{x_j < x_i} d(x_j) \right) \geq d(x_j) $$

The last step follows from the fact that the max over a set of elements is larger than any individual element.

The case of $@ x_j \geq x_i $@ is proved similarly.

Thus, we've shown that whenever $@ x_i > x_j $@, $@ d(x_i) > d(x_j) $@.

**Endproof.**

As an example of how this works, consider the choices $@ \\{ \textrm{Priyanka}, \textrm{Sandeep}, \textrm{Nithin}, \textrm{Sneha} \\} $@. We first define:

$$ d(\textrm{Priyanka}) \equiv 0 $$

Now we consider Sandeep. We observe that $@ \textrm{Sandeep} > \textrm{Priyanka} $@. As a result, we apply rule (1) to find:

$$ d(\textrm{Sandeep}) \equiv d(\textrm{Priyanka}) + 1 = 1$$

Now consider Nithin. We have that $@ \textrm{Priyanka} < \textrm{Nithin} < \textrm{Sandeep} $@. As a result, rule 4 applies:

$$ d(\textrm{Nithin}) = \frac{1}{2} \left( d(\textrm{Priyanka}) + d(\textrm{Sandeep}) \right) = \frac{1}{2}(0 + 1) = \frac{1}{2} $$

Finally we note that $@ \textrm{Sneha} \sim \textrm{Priyanka} $@, so we assign:

$$ d(\textrm{Sneha}) \equiv d(\textrm{Priyanka}) = 0 $$

Checking that the metric agrees with the underlying decision process is left as an exercise for the reader. And I really mean that - if you had trouble understanding the proof above, please work through this example. The example will illustrate fairly clearly why managing by metric is equivalent to managing by

# Conclusion

Elementary topology shows that a good decisionmaking process is equivalent to managing by metric. Yet in the real world, many people oppose metric-based management. Hopefully this blog post will serve to change the opinions of those misguided souls.

If this theorem fails to persuade, then I ask the following question: indecision, inconsistency, or subjectivity - which one are you advocating for?
