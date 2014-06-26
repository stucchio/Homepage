 title: Topological fact - making decisions by the numbers is the only way to go
date: 2014-06-30 09:00
author: Chris Stucchio
tags: metrics, data analysis, topology
status: draft
mathjax: true

Humans don't like to be measured. "You can't reduce a person to a single number!" is a popular critique. The reactions against metric-based decisions are almost visceral in many cases. Standardized tests in schools are widely criticized. In the office, managing workers by metrics is wildly unpopular. However, most of these critiques are simply misguided - the alternative to metric driven decision making is not heaven on earth. It's merely subjective or inconsistent decision making.

That's not an opinion. That's a mathematical fact. It's an exercise in elementary topology.

# Management by metric - in mathematical terms

We define management by metric to be the following decision process. Consider the set of choices $@ X $@. Then there is a metric, i.e. a function $@ d : X \rightarrow \mathbb{R} $@ which reduces each choice to a single number. Whenever

$$ d(x) > d(y) $$

we choose $@ x $@ over $@ y $@. We also assume the function $@ d(x) $@ to be deterministic - it always returns the same answer.

# Properties of a good decision process

The first important property of a decision process is that it should always work. To begin with, let us consider two choices $@ x $@ and $@ y $@. We will write

$$ x \leq y $$

if our decision process says the choice $@ y $@ is not inferior to $@ x $@. We will write

$$ x \sim y $$

whenever both $@ x \leq y $@ and $@ y \leq x $@. Whenever this is true, the decision process says we can choose $@ x $@ or $@ y $@ at random - it will make no difference.

## Property 1: Decisiveness (aka totality)

The first property a decision process should have is that it actually makes a decision. I.e., for every possible choice $@ x $@ and $@ y $@, either

$$ x \leq y \textrm{ or } y \leq x .$$

This does not mean the decision process can always determine the best choice. It merely means that it can make *some* choice.

## Property 2: Consistency (aka transitivity)

The second important property a decision process should have is consistency. This means:

$$ \textrm{ if } x \leq y \textrm{ and } y \leq z \textrm { then } x \leq z $$

In mathematics this property is called transitivity. This feature is important. Suppose you are hiring someone, and you need to choose between Priyanka, Sandeep and Nitin. Suppose you prefer Sandeep to Priyanka and Nitin to Sandeep. If your decision process is consistent, you can now conclude that you prefer Nitin to Priyanka.

On the other hand, suppose your process was not consistent, and you prefer Priyanka to Nitin. Now what? Who do you hire?

## Property 3: Objectivity (aka determinicity)

Objectivity simply means that your decision process works and gives the same answer regardless of who is running it. This is less a mathematical point  and more a computer science point - it means your decision process is deterministic.

# Here comes the topology

One of the earliest topics studied in topology is the study of orderings. An ordering is a relation, like our $@ \leq $@ relation above. There are a variety of types of relations, each satisfying more stringent assumptions.

A preorder is simply a relation which satisfies reflexivity (namely $@ x \leq x $@) and consistency (aka transitivity). A partial order adds the requirement of antisymmetry - if $@ x \leq y $@ and $@ y \leq x $@ then $@ x = y $@. A [total order](http://en.wikipedia.org/wiki/Total_order) is a partial order together with the decisiveness property.

The decision process I'm describing in this post satisfies all the properties of a total order except for antisymmetry.

So here is the fun topological fact.

**Theorem:** Suppose you have a decisive, consistent and objective method of making decisions. Suppose further that the set of decisions is no more than countably infinite. Then there exists a metric $@ d : X \rightarrow \mathbb{R} $@ with the property that:

$$ d(x) > d(y) \textrm{ if and only if } x \geq y $$

In words, this means whenever you have a decisive, consistent and objective decision process, then someone else can make the *exact same decisions* if they are managing by metric (for some particular metric).

I'm writing this as a mathematical proof, but I urge the reader to bear with me. The proof is fairly simple induction/recursion, and hopefully should be accessible to anyone with a computer science background.

**Proof:** The goal here is to show that whenever we have a decisive, consistent and objective process, we are managing by metric. To do this, we must build the metric function $@ d(x) $@.

To begin, number the possible choices $@ x_0, x_1, x_2, \ldots $@. Then define:

$$ d(x_0) = 0. $$

Now, for $@ i \geq 1 $@, we define $@ d(x_i) $@ as follows.

1. If $@ x_i > x_j $@ for every $@ j < i $@, then we define $@ d(x_i) = \max_{j < i} d(x_j) + 1 $@.
2. If $@ x_i < \min_{j < i} x_j $@, then we define $@ d(x_i) = \min_{j < i} d(x_j) - 1 $@.
3. If $@ x_i \sim x_j $@ for any $@ j < i $@, then we define $@ d(x_i) = d(x_j)$@.
4. If none of the above conditions are satisfied, then we define:
$$ d(x_i) = \frac{1}{2} \left( \max_{x_j < x_i} d(x_j) + \min_{x_j > x_i} d(x_j) \right)$$

In the last case, we are simply collecting all the items smaller than $@ x_i $@, all the iterms bigger than $@ x_i $@, and assigning $@ d(x_i) $@ to the midoint of the region between those.

We now need to show that if $@ x_j < x_i $@, then $@ d(x_j) < d(x_i) $@. This means that using our decision process is equivalent to managing by metric, for the specific metric $@ d $@.

1. We have that $@ x_i > x_j $@ for every $@ j < i$@. Clearly $@ d(x_i) = \max_{j < i} d(x_j) + 1 > d(x_j) $@.
2. Just flip around the previous case.
3. Suppose $@ x_i \sim x_j $@. Since $@ d(x_i) = d(x_j) $@, then $@ d(x_i) \leq d(x_j) $@ and $@ d(x_i \geq d(x_j) $@ we are done.
4. For any $@ x_j \leq x_i $@, we have:

$$ d(x_i) = \frac{1}{2} \left( \max_{x_j < x_i} d(x_j) + \min_{x_j > x_i} d(x_j) \right) \geq \frac{1}{2} \left( \max_{x_j < x_i} d(x_j) + \max_{x_j < x_i} d(x_j) \right)$$
$$ \geq \left( \max_{x_j < x_i} d(x_j) \right) \geq d(x_j) $$

The last step follows from the fact that the max over a set of elements is larger than any individual element.

The case of $@ x_j \geq x_i $@ is proved similarly.

Thus, we've shown that whenever $@ x_i > x_j $@, $@ d(x_i) > d(x_j) $@.

**Endproof.**

**NOTE:** other people use inconsistency to mean "changing your beliefs based on new information". http://www.huffingtonpost.com/joel-gascoigne/the-habits-of-successful-_b_4561752.html
