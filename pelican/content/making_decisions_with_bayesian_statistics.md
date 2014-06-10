title: Making decisions with Bayesian Statistics - A Tutorial
date: 2014-06-15 09:30
author: Chris Stucchio
tags: ab testing, bayesian statistics, ab testing
mathjax: true
summary: Bayesian Statistics allows you to take data and a prior belief, and compute a probability distribution (the posterior) describing your beliefs about the world. But how do you make decisions based on that data? This post explains how.


Recently, Bayesian A/B testing has been gaining some popularity. The startup Lyst has release a [tool for computing posteriors](http://developers.lyst.com/bayesian-calculator/), and Evan Miller has derived some nice simple formulas for [computing P(ctr_A > ctr_B)](http://www.evanmiller.org/bayesian-ab-testing.html). But so far everyone is missing an important piece of the puzzle - a [decision rule](http://en.wikipedia.org/wiki/Decision_rule). A decision rule is a function which turns data into action - it's the piece of code which tells us "A/B test is over, choose B."

In this post I'll provide a framework describing how to use a Bayesian decision rule, and I'll show how to use this framework for the example of measuring conversion rates.

In order to make this post hopefully accessible both to math geeks and programmers, I'll attempt to explain the concepts both in terms of math constructs and in (occasionally oversimplified) computer constructs. The pseudocode I write is inspired by Julia, but with more accurate type signatures.

# Step 1: A model of the world

Before a test begins, we must formulate a mathematical model of the world. This model is semi-deterministic, and describes how the world works. To begin our rolling example, let us consider conversion rates.

**Model:** I believe that both call to actions A and B have a well defined *conversion rate*. I.e.:

$$ P(\textrm{conversion} | \textrm{user views A}) = p_a $$

and

$$ P(\textrm{conversion} | \textrm{user views B}) = p_b $$

The values $@ p_a, p_b$@ do not change over time, and will remain valid once the experiment is finished.
**End model**

This model expresses a clear view about the world. It does not assert that we know $@ p_a $@ and $@ p_b $@, it merely asserts that they both exist. This is the simplest possible model, but others are possible.

The values which represent the model are called *parameters*. In the interests of clearly representing what is needed, we will describe them as having type `Param`. For example, in the conversion rate example:

```julia
type Param = (Float64, Float64)
```

# Step 2: A *prior* opinion

Before a test begins, we must have some *opinion* about what the world looks like. This opinion is represented by a probability distribution on possible states of the world. In mathematical terms this is a function $@ f_{prior}(\theta) $@ with the property that:

$$ \int f_{prior}(\theta) d\theta = 1. $$

For the example of conversion rates above, one possible choice is $@ f_{prior}(\theta) = 1 $@. This represents the opinion that all conversion rates are equally likely.

In programming terms, you can also think of a probability distribution as being a function together with a discrete set of possible values.:

```julia
type ProbabilityDistribution
  parameterChoices :: Array{Param, 1} # Parameter choices is an array of legitimate Param values
  f :: Function{Param,Float64}
end
```

It must satisfy the property that:

```
sum(f(parameterChoices)) === 1.0
```

For a very concrete example, let us consider again conversion rates:

```julia
parameterChoices = [0.0, 0.01, 0.02, ..., 0.99]
```

The function `f` might then be:

```julia
function f(x)
  return 1.0 / 100.0
end
```

This again represents the opinion that all conversion rates are equally likely. The reason we divide by `100` is that our grid `parameterChoices` has `100` elements.

# Step 3: Evidence and how to change your opinion
