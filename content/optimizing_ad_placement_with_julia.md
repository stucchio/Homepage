title: Optimizing Ad Placement with Julia and Maximum Likelihood
date: 2014-05-19 09:00
author: Chris Stucchio
tags: conversion rates, statistics, julia
mathjax: true





Estimating the conversion rate of an advertisement placed in a fixed slot on a webpage is a well studied problem, and one I've [discussed](/blog/2013/bayesian_analysis_conversion_rates.html) [at length](/blog/2013/bayesian_bandit.html). For those who haven't seen, here are some [slides](/pubs/slides/helpshift_2014/slides.html) which might help.

In the real world, however, it's not always the case that an advertisement will always appear in the same slot. Frequently there are multiple slots on page where an ad might appear - the navigation bar on top, the right rail (the vertical bar to the right side of the page), after the post content, and perhaps others. How can we handle this situation? If we have a lot of data this is a very simple problem - compute `ctr['topnav'] = clicks['topnav'] / displays['topnav']`, `ctr['rightrail'] = clicks['rightrail'] / displays['rightrail']`, etc.

If we do not have a lot of data, we would like to relate the conversion rate in one location with that in the others so that we can take advantage of all the data we have. In this blog post I'll describe the simplest possible statistical method for addressing this problem, and provide an implementation in the Julia language.




# A simple model

The first thing to recognize is that we must assume there is some sort of relationship between `ctr['rightrail']` and `ctr['topnav']` for a fixed ad. If there is no such relationship, then we have no hope of making any inference about `ctr['rightrail']` given knowledge of `ctr['topnav']` - the two quantities are simply unrelated. The simplest way of relating the conversion rates in each location with each other is via a linear model.

Specifically, we'll assume that the click through rate of an ad in a given location is the product of two factors - the visibility of the location, and the quality of the ad.

To begin with, let the variable $@ i=1 \ldots N $@ represent the slot - perhaps $@ i=1 $@ is the top navbar, $@ i=2 $@ is the right rail, etc.

In this model, we assume that for each advertisement there is a fixed quantity $@ z \in [0,1] $@ which represents the *quality* of an ad. There is also a set of *slot parameters* $@ \alpha_i $@, satisfying $@ \alpha_1 = 1.0 $@ and $@ \alpha_i \geq \alpha_{i+1} $@. We then assume that conversion rates are governed by:

$$ \textrm{ctr}_i = \alpha_i z $$

What this means is that the click through rate of an ad is proportional to both the quality of the ad and the visibility of the slot in which it is placed.

We haven't made as many assumptions here as it looks like. The constraint that $@ \alpha_i \geq \alpha_{i+1} $@ merely demands that we order the slots from most performant to least. And the constraint that $@ z \in [0,1] $@ and $@ \alpha_1 = 1.0 $@ is derived from the fact that click through rates must be between 0 and 1, and they can be as large as 1.

Now suppose we've displayed an ad in all the slots a number of times. The result of this will be two vectors, the *click* vector

$$ \vec{c} = [c_1, c_2, \ldots, c_n ] $$

where $@ c_i $@ represents the number of clicks received in slot $@ i $@ and the *show* vector

$$ \vec{s} = [s_1, s_2, \ldots, s_n ] $$

where $@ s_i $@ represents the number of times the ad was displayed in slot $@ i $@.

At this time I'll simply take the values $@ \alpha_i $@ to be known quantities. I'll return to the actual computation of them later on.

## Optimizing Ad Placement

Now suppose that we have a sequence of advertisements, each of which we have measured to have quality scores of $@ z_1, \ldots, z_M $@ (where possibly $@ M \neq N $@). The optimal way to place the ads is to put the highest quality ad in the highest quality slot, the second highest quality ad in the second best slot, etc.

So our goal is to compute $@ z_j $@ for each advertisement and then put the best ads in the best slots.

# Likelihood

The *likelihood* of an event $@ e $@, given a parameter $@ z $@, is the probability of that event occuring given the parameter value $@ z $@ - i.e., $@ P( \textrm{event} | z ) $@. We denote this by $@ L(e | z) $@.

Suppose we display an ad in slot $@ i $@, and a click occurs. The likelihood of this event is:

$$ L( \textrm{click in slot } i | z ) = \alpha_i z $$

This is true simply because by definition $@ \alpha_i z $@ is the clickthrough rate of an advertisement in slot $@ i $@. Similarly:

$$ L( \textrm{no click in slot } i | z ) = 1 - \alpha_i z $$

More generally, if we display an at $@ s_i $@ times and it is clicked on $@ c_i $@ times, then the likelihood is given by the [binomial distribution](http://en.wikipedia.org/wiki/Binomial_distribution):

$$ L( c_i, s_i | z ) =  {s_i \choose c_i}(\alpha_i z)^{c_i}(1-\alpha_i z)^{s_i-c_i} $$

Finally, aggregating data across all slots, the likelihood would be:

$$ L( \vec{c}, \vec{s} | z ) = \prod_{i=1}^n {s_i \choose c_i} (\alpha_i z)^{c_i}(1-\alpha_i z)^{s_i-c_i} $$

# Maximum likelihood

We now have a set of data, together with a model that purports to predict the distribution of that data. What we really want is a way of computing the model parameters - in this case, $@ z $@.

A popular frequentist technique for doing this is maximum likelihood. Maximum likelihood considers all possible values of $@ z $@ and chooses the the one that makes what *actually* happened the *most likely* thing to have happened:

$$ \textrm{argmax}_{z} L( \vec{c}, \vec{s} | z ) $$

**Fact 1:** Computing the maximum likelihood is equivalent to computing the maximum *log-likelihood*:

$$ \textrm{argmax}_{z} \ln\left[ L( \vec{c}, \vec{s} | z ) \right] $$

This is because the function $@ \ln(x) $@ is monotonically increasing in $@ x $@ - making the likelihood bigger always makes the log bigger.

This is an important fact to note because it drastically simplifies the computations. To actually maximize the likelihood, we'll be using [gradient descent](http://en.wikipedia.org/wiki/Gradient_descent), which requires computing derivatives of the objective function. If we wish to compute the derivative of $@ L(\vec{c}, \vec{s} | z) $@, we must repeatedly use the product rule.

In contrast, consider the log-likelihood:

$$ \ln[ L( \vec{c}, \vec{s} | z )] = \ln \left[ \prod_{i=1}^n {s_i \choose c_i} (\alpha_i z)^{c_i}(1-\alpha_i z)^{s_i-c_i} \right] $$
$$ = \ln\left[\prod_{i=1}^n {s_i \choose c_i} \right] + \ln \left[\prod_{i=1}^n (\alpha_i z)^{c_i}(1-\alpha_i z)^{s_i-c_i} \right] $$
$$ = \ln\left[\prod_{i=1}^n {s_i \choose c_i} \right] + \sum_i \left[ c_i \ln(\alpha_i z) + (s_i-c_i) \ln(1-\alpha_i z) \right] $$

This is a helpful simplification because it makes computing derivatives easier:

$$ \frac{ d\ln[ L( \vec{c}, \vec{s} | z )] }{dz} = 0 + \sum_i \left[ \frac{c_i}{z} - \frac{\alpha_i(s_i-c_i)}{1-\alpha_i z} \right] $$

## Implementing it in Julia

We can define the logLikelihood function in Julia as follows:

    function logLikelihood(z::Float64, clicks::Array{Float64,1}, shows::Array{Float64,1}, alpha::Array{Float64,1})
        @assert size(clicks) == size(shows)
        @assert size(shows) == size(alpha)
        return sum(clicks .* log(z*alpha) .+ (shows .- clicks) .* log(1-z*alpha))
    end

The `.*` operator represents element-wise multiplication, `.+` elementwise addition, etc. Note that this computation completely ignores the $@ {s_i \choose c_i} $@ term - that's because it's a constant. It does not change the *location* of the maximal log-likelihood - merely the value at that point.

Similarly, `log(az)` behaves like a numpy or breeze UFunc - it computes the logarithm element-wise across the array. The `sum` function them adds up all the elements in the array.

We can define the derivative similarly:

    function derivLogLikelihood(z::Float64, clicks::Array{Float64,1}, shows::Array{Float64,1}, alpha::Array{Float64,1})
        @assert size(clicks) == size(shows)
        @assert size(shows) == size(alpha)
        return sum((clicks / z) .- alpha .* (shows .- clicks) ./ (1 .- (alpha*z)))
    end

Julia has the [Optim](https://github.com/JuliaOpt/Optim.jl) package available which provides an `optimize` function, which can be implemented via gradient descent or other methods. Unfortunately, the `optimize` function does not allow the domain of the variable being optimized to be constrained. So although we know that $@ z \in [0,1] $@, the `optimize` function might return negative numbers, or attempt to use negative numbers at intermediate stages of the computation.

This is bad. The problem here is that the Julia library we use doesn't directly recognize the mathematics of the underlying problem.

To prevent this, we must *reparamaterize* the problem. We do this by defining a new variable $@ y = \tan(\pi z - \pi/2) $@. The variable $@ y $@ can be any real number - this means that if Julia's optimization library gives us an answer of 738.2, we can make sense of it. We can then take the y-value and map it back to a $@ z $@ values in $@ [0,1] $@. In Julia we do this as follows:

    function yToZ(y::Float64)
        return 0.5+atan(y)/pi
    end

    function zToY(z::Float64)
        return tan(pi*z-(pi/2.0))
    end

**Fact 2:** Finding the variable $@ y $@ maximizing $@ \ln[L(\vec{c}, \vec{s} | 0.5+\pi^{-1} \arctan(z) )] $@ is equivalent to finding $@ z $@ maximizing $@ \ln[\L(\vec{c}, \vec{s} | z)] $@.

However, this changes the optimization problem. We must now compute gradients with respect to $@ y $@ rather than with respect to $@ z $@. This is easily accomplished via the chain rule:

$$ \frac{ d\ln[ L( \vec{c}, \vec{s} | z(y) )] }{ dy } = \frac{ d\ln[ L( \vec{c}, \vec{s} | z )] }{ dz } \frac{dz}{dy} = \frac{ d\ln[ L( \vec{c}, \vec{s} | z )] }{ dz } \frac{\pi^{-1}}{1+y^2} $$

Because of this, we don't even need to rewrite our objective functions or derivatives. We merely need to write a new function:

    function dzdy(y::Float64)
        return (1.0/pi) / (1+y*y)
    end

Now we are ready to actually find `y`, and similarly find `z`.

Then, given data on `click`, `show` and `alpha`, we build a function to compute $@ - \ln[ L( \vec{c}, \vec{s} | z )] $@. We compute the negative of this because the `optimize` function in Julia *minimizes* rather than maximizes it's argument. So we define the objective function as follows:

    function f(y::Array{Float64,1})
        return -1*logLikelihood(yToZ(y[1]), clicks, shows, alpha)
    end

The value `y` is passed in as an array because that is what the `optimize` function expects.

The function to compute the derivative of `f` mutates an in-place array rather than returning a new one. So we define the derivative of the objective function as follows:

    function df!(y::Array{Float64,1}, storage::Array{Float64,1})
        storage[1] = -1*derivLogLikelihood(yToZ(y[1]), clicks, shows, alpha) * dzdy(y[1])
    end

This strange structure is designed to avoid memory allocation in the event of higher dimensional gradients.

Finally, we are ready to optimize:

    result = optimize(f, df!, [0.0], method = :gradient_descent)

The `result` object contains quite a bit of information on the optimization result. The actual parameter `z` is computed via:

    z = yToZ(result.minimum[1])

Code which implements this can be found [here](https://gist.github.com/stucchio/66bd9af4314499f0c436).

# How to compute $@ \alpha_i $@

In order to find $@ \alpha_i $@, we need to run some experiments. In these experiments we will run multiple advertisements in multiple slots, and gather data on how each one performs. This should be done on a fairly large and representative set of ads.

Once we gather this data, we can use maximum likelihood to *simultaneously* compute both $@ \alpha_i$@ and $@ z_j $@ for the experiment. If the experiment is large enough this will likely be a good estimator of $@ \alpha_i $@. Once the $@ \alpha_i $@ is computed, we can then use it in the future for optimization as per the above analysis.

## Maximum likelihood for multiple experiments

To begin with, we first need to compute the log-likelihood function over a sequence of experiments with different $@ z_j $@. The log-likelihood (ignoring additive constants) is:

$$ \sum_j \sum_i \left[ c_{i,j} \ln(\alpha_i z_j) + (s_{i,j}-c_{i,j}) \ln(1-\alpha_i z_j) \right] $$

Because of the constraints we've imposed on $@ \alpha $@, simply running a stock optimization method on it will not work well. There is nothing preventing $@ \alpha_1 $@ from being unequal to 1.0, or preventing $@ \alpha_3 $@ from being larger than $@ \alpha_2 $@. So if we use the standard Julia optimization methods, we could very easily wind up with $@ \vec{\alpha} $@ not satisfying our constraints.

In order to prevent this in a fairly natural way, we must re-parameterize the problem so that the constraints are automatically preserved. To do this, we define:

$$ \alpha_1 = 1.0 $$
$$ \alpha_i = \prod_{j=2}^i \beta_j $$

We'll then attempt to find $@ (\vec{z}, \vec{\beta}) $@ for which likelihood is maximized.

Computing derivatives with respect to these variables yields:

$$ \frac{\partial}{\partial \beta_k} \sum_j \sum_i \left[ c_{i,j} \ln(\alpha_i z_j) + (s_{i,j}-c_{i,j}) \ln(1-\alpha_i z_j) \right] = $$

$$ \sum_{i \geq k} \sum_j \frac{c_{i,j}}{\beta_k} - \frac{ (s_{i,j} - c_{i,j}) z_j (\alpha_i / \beta_k ) }{1-\alpha_i z_j} $$

Similarly:

$$ \frac{\partial}{\partial z_j} \sum_j \sum_i \left[ c_{i,j} \ln(\alpha_i z_j) + (s_{i,j}-c_{i,j}) \ln(1-\alpha_i z_j) \right] = $$

$$ \sum_i \left[ \frac{c_{i,j}}{z_j} - \frac{(s_{i,j}-c_{i,j})\alpha_i}{1-\alpha_i z_j} \right] $$

We can now build it in Julia.

## Julia implementation

The implementation of maximal likelihood in Julia is straightforward - you can [view it here](https://gist.github.com/stucchio/66bd9af4314499f0c436#file-mle_find_alpha-jl). It achieves results that appear correct at first glance:

    clicks = [ 25 13 10; 20 9 4; 10 4 1; 12 4 0]
    shows = [ 100 105 97; 99 103 96; 102 100 101; 103 101 107]

This represents a situation with 3 slots and 4 advertisements. Ad #1 achieved a 25/100 clicks in slot 1, 13/105 in slot 2 and 10/97 in slot 3, similarly for ads 2-4.

    (alpha, z) = computeAlphaZ(clicks, shows)

After this, the result is:

    alpha == [1.0,0.45101141823350566,0.22593041690511678]
    z = [0.2784097973476466,0.1978200091513846,0.08869000396718513,0.09368066187975937]

This intuitively makes sense. The click through rate in slot 2 appears to be half of that in slot 1, and in slot 3 is about half of that in slot 2. Similarly, the click through rate of the first two advertisements appears to be about twice that of the second, and the maximal likelihood estimate roughly agrees.

### Non-robust implementation

An unfortunate fact about the implementation is that it doesn't seem very robust. Occasionally repeating it yields errors:

    ERROR: assertion failed: :((dphia<0))
     in secant2! at /home/stucchio/.julia/v0.2/Optim/src/linesearch/hz_linesearch.jl:438
     in hz_linesearch! at /home/stucchio/.julia/v0.2/Optim/src/linesearch/hz_linesearch.jl:355
     in hz_linesearch! at /home/stucchio/.julia/v0.2/Optim/src/linesearch/hz_linesearch.jl:201
     in gradient_descent at /home/stucchio/.julia/v0.2/Optim/src/gradient_descent.jl:93
     in optimize at /home/stucchio/.julia/v0.2/Optim/src/optimize.jl:312
     in computeAlphaZ at /home/stucchio/src/webpage/content/blog/2014/optimizing_ad_placement_with_julia/mle_find_alpha.jl:89
     in include at boot.jl:238
     in include_from_node1 at loading.jl:114
     in process_options at client.jl:303
     in _start at client.jl:389
    at /home/stucchio/src/webpage/content/blog/2014/optimizing_ad_placement_with_julia/mle_find_alpha.jl:99

Sometimes:

    ERROR: assertion failed: :((lsr.slope[ia]<0))
     in update! at /home/stucchio/.julia/v0.2/Optim/src/linesearch/hz_linesearch.jl:522
     in hz_linesearch! at /home/stucchio/.julia/v0.2/Optim/src/linesearch/hz_linesearch.jl:383
     in hz_linesearch! at /home/stucchio/.julia/v0.2/Optim/src/linesearch/hz_linesearch.jl:201
     in gradient_descent at /home/stucchio/.julia/v0.2/Optim/src/gradient_descent.jl:93
     in optimize at /home/stucchio/.julia/v0.2/Optim/src/optimize.jl:312
     in computeAlphaZ at /home/stucchio/src/webpage/content/blog/2014/optimizing_ad_placement_with_julia/mle_find_alpha.jl:89
     in include at boot.jl:238
     in include_from_node1 at loading.jl:114
     in process_options at client.jl:303
     in _start at client.jl:389
    at /home/stucchio/src/webpage/content/blog/2014/optimizing_ad_placement_with_julia/mle_find_alpha.jl:99

I don't know if this is caused by the fact that the data is underdetermined, or because of some flaw in my implementation. A more robust set of codes would be nice. I probably won't build it myself since I tend to use Bayesian methods, but it's worth emphasizing this drawback of my implementation.

# Conclusion

I've just gotten started playing with it, but [Julia](http://julialang.org/) is pretty nice for a scientific language. Unlike [many](http://www.r-project.org/) [other](http://www.mathworks.in/products/matlab/) [products](http://www.maplesoft.com/products/maple/), Julia is actually a decent general purpose programming language.

They make odd choices like 1-indexing for arrays, but overall it's a fairly nice little scripting language. They have [lispy macros](http://docs.julialang.org/en/release-0.2/manual/metaprogramming/), a fairly simple [type system](http://docs.julialang.org/en/release-0.2/manual/types/) and a good [ffi](http://docs.julialang.org/en/release-0.2/manual/calling-c-and-fortran-code/). I don't have strong opinions on Julia yet, but I'm thinking that it might make a nice replacement for Python.
