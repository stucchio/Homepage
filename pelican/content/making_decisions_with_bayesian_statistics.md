title: Making decisions with Bayesian Statistics - A Tutorial
date: 2014-06-15 09:30
author: Chris Stucchio
tags: ab testing, bayesian statistics, decision rules
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

The programming formulation is not identical to the mathematical formulation, but it's similar enough that you won't make too many mistakes.

# Step 3: Evidence and how to change your opinion

Now suppose we've run an experiment. An experiment consists of making observations about the world. A key point in an experiment is that the probability of these observations being made is different for different parameter choices.

Consider the conversion rate example above. Suppose we display call to action A to two users, and both of them click. The probability of this occurring is $@ p_a^2 $@ - this value changes depending on $@ p_a $@. You can then compute a *posterior* probability using Bayes rule:

$$ P(\theta|\textrm{evidence}) = \frac { P(\textrm{evidence} | \theta) P(\theta) } { P(\textrm{evidence}) } $$

The value $@ P(\textrm{evidence} | \textrm{Param}) $@ is determined simply by the model you specified in step 1. The value $@ P(\textrm{Param}) $@ is your prior. The value $@ P(\textrm{evidence}) $@ can be computed via the integral:

$$ P(\textrm{evidence}) = \int P(\textrm{evidence} | \theta) P(\theta) d \theta $$

In programming terms, we do the following:

```julia
function posterior(evidence, prior)
    normalization = 0.0

    for i = 1:prior.parameterChoices.length
      normalization += prior.f(prior.parameterChoices[i]) * probability_of_evidence_given_param(evidence, prior.parameterChoices[i])
    end

    function g(x)
      return f(x) * probability_of_evidence_given_param(evidence, x) / normalization
    end

    return ProbabilityDistribution(prior.parameterChoices, g)
end
```

The function `probability_of_evidence_given_param(evidence, x)` comes from your model. For example, in the case of conversion rates:

$$ P(\textrm{evidence} | \theta) = \theta^{c}(1-\theta)^{n-c} $$

```julia
function probability_of_evidence_given_param(num_conversions, num_shows, x)
  return (x^num_conversions) * ((1-x)^(num_shows-num_conversions))
end
```

# Step 4: Cut your losses

At this point we need to introduce a *loss function*. A loss function is a function $@ L(\theta, D) $@ which represents how much you will lose by making decision $@ D $@ if the true value of the parameter were $@ \theta $@.

Lets make this very clear by going back to our example of choosing conversion rates. In this example, $@ \theta = (p_a, p_b) $@. If we make the wrong decision, say choosing B when the better version was A, our loss will be $@ p_a - p_b $@.

$$ L( (p_a, p_b), \textrm{choose A}) = \max \left( p_b - p_a, 0 \right) $$

$$ L( (p_a, p_b), \textrm{choose B}) = \max \left( p_a - p_b, 0 \right) $$

What this means is that if we choose A, and $@ p_b > p_a$@, then we've made a mistake. As a result of our mistake, we lose an amount proportional to the conversions we failed to gain.  However, if $@ p_a > p_b$@, we lose nothing. The same applies if we choose B, but in reverse.

Now the loss function gives the loss for a fixed value of $@ \theta $@, but what we really want is the *expected loss*. This is computed with the help of the posterior:

$$ L(D) = \int L( \theta, D) P(\theta | \textrm{evidence}) d\theta $$

**Your mission:** Come up with a strategy, based on the evidence, which computes a decision to minimize the expected loss. In the Bayesian context, this will typically be a function that takes as input the posterior, and returns as output a decision.

A strategy I often use for A/B testing is the following. I choose a "threshold of caring" - a value $@ \epsilon $@ below which I don't care about differences between A and B. Then at each step, I check if:

$$ L(A) = \int L( \theta, A) P(\theta | \textrm{evidence}) d\theta \leq \epsilon $$

If so, I choose B - this is because the error I expect from choosing A is so low that I don't care. Conversely, if:

$$ L(B) = \int L( \theta, B) P(\theta | \textrm{evidence}) d\theta \leq \epsilon $$

then I would choose A.
