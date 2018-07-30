title: Alien Intelligences and discriminatory algorithms
date: 2016-03-21 10:00
author: Chris Stucchio
tags: bias detection, frequentist statistics, statistics
category: ai ethics
mathjax: true

![let that be your last battlefield](/blog_media/2016/is_your_algorithm_discriminatory/star_trek.png)

In the Star Trek episode [Let That Be Your Last Battlefield](https://en.wikipedia.org/wiki/Let_That_Be_Your_Last_Battlefield) the Enterprise encounters two human-looking aliens (as is the Star Trek custom) from the planet Cheron. These aliens are full of intense ethnic hatred towards each other based on historical issues on their planet. This episode was broadcast in 1969; to a 2016 TV watcher like myself it comes off as a ham-handed criticism of American racial attitudes at the time. We, the human viewers, are of course oblivious to whatever happened on Cheron prior to this episode - most likely the human readers of my blog didn't notice that the Cheronese are mirror images of each other. As a result we find the hatred and conflict between the two Cheronese completely nonsensical.

As aliens to the Cheronese, we (either the viewer or Captain Kirk) just don't care. Insofar as we might favor one Cheronese over the other, that would only be due to the danger or reward to the Enterprise. Captain Kirk cares about protecting the ship and discovering new life and new civilizations - minor aesthetic differences between two people from the same civilization are irrelevant to him.

On Star Trek the majority of the aliens are just humans with colored makeup. In real life aliens will be truly different. One very important category of "alien" is machine learning - machine learning algorithms are completely alien to us and this fact is unfortunately lost on a lot of innumerate journalists.

As AI-driven decisions are becoming more commonplace (e.g. in predicting crime, creditworthiness, advertisement delivery), pundits and journalists have [become](http://www.nytimes.com/2015/09/25/us/police-program-aims-to-pinpoint-those-most-likely-to-commit-crimes.html?_r=0) [increasingly](http://techcrunch.com/2015/08/02/machine-learning-and-human-bias-an-uneasy-pair/) [concerned](https://www.schneier.com/blog/archives/2016/01/replacing_judgm.html) that such algorithms might be "discriminatory" against various special classes of humans. Typically these pundits attribute to algorithms various human qualities; the mere ability to discriminate by race is treated as an assumption that the algorithm is doing so and in the same way that humans would. Cathy O'Neil - aka [mathbabe](http://mathbabe.org/) - is one of the foremost writers in this field. In spite of her blog's title, she uses negligible amounts of math but lots of emotional rhetoric to groundlessly criticize statistics in order to sell books.

Unfortunately this is all a load of anthropomorphic nonsense. Algorithms aren't people. While humans are known to be easily biased on physical traits of other humans, algorithms aren't. To a human, "race" or "sex" is a fundamental trait of another person. An algorithm cares about the 26'th element of a 100 element array as much as Kirk cares about who is black on the left - if it's predictive of something he cares about he'll pay attention, otherwise he doesn't care. It's a fair criticism that algorithms can reproduce biases in their inputs. But the *assumption* that they will do this - just like humans do - is fundamentally flawed.

In reality, if the inputs to an algorithm are sufficiently informative, the algorithm will *correct* the bias in the inputs!

This post is going to be somewhat mathematical. Unfortunately, while it's easy to criticize algorithms on emotional and anthropomorphic terms, it's very hard to defend them on that basis. So I'm going to introduce and explain linear regression - the simplest machine learning algorithm that I can think of - and show what conditions lead to algorithmic discrimination.

## What this article is about

This article is about *when* and *why* an algorithm would discriminate, and more importantly when it *won't*. To illustrate this I'm going to construct a few hypothetical worlds, run an algorithm on that hypothetical world, and illustrate the output. By inverting this process, we can conclude that *if* an algorithm behaves a certain way, that is evidence that the *world* behaves in a corresponding manner (this is the uncomfortable part).

At the end I also discuss some ethical issues, but I take no particular position. My main goal here is to push discussion of this issue in a less innumerate direction.

### What this article is NOT about

This article is strictly NOT about badly implemented algorithms. Most of the people commenting on algorithmic discrimination are not arguing that a specific algorithm has an off-by-one error or proposing that we switch from a random forest to a deep neural network. I've never seen any LaTeX on mathbabe.org. In the event that an algorithm is *incorrectly* predicting outcomes, we can all agree that statisticians should do their jobs better.

All the simulation experiments in this article will be carefully tuned to avoid this situation. I'll be generating gaussian data and fitting a linear model to it via least squares. The key point here is to avoid methodological errors - because I'm setting up the problem to be simple and easily solvable, you can't get a significantly better result via better algorithm choices. Instead, we'll need to actually recognize and confront the reality that good algorithms might yield correct results we don't like.

I'm very strictly NOT claiming that all real world models are perfect. I'm just assuming that bad models are a math problem with a math solution and therefore beyond the reach of Techcrunch and Mathbabe.

## Different kinds of discrimination

To begin with, we need to define what we mean by discrimination, and unfortunately there are several definitions floating around.

**Direct Discrimination:** This form of discrimination is basically traditional racism - you encode your preferences into a model. However, this is pretty uncommon in more formal predictive models. When writing code, very few data scientists will write this:

```python
if applicant.race == 'black':
    fico -= 100
```

That's certainly something that will be spotted in code review, and it's also pretty easy to prevent with automated tools, e.g.:

```python
for a in applicants:
    a.race = None
predictive_algorithm(applicants)
```

I'm going to call a data set without direct information on protected classes **scrubbed**.

**Disparate Impact:** This is when you have an unbiased algorithm, but the outcome of that algorithm is affects different protected classes differently. Direct discrimination can certainly cause a disparate impact, but there are lots of other possible causes. For example, if black people are taller than white people, a basketball competition will have a disparate inpact in their favor.

**Redundant encoding:** This is what happens when you give an algorithm lots of data, and ask it to learn hidden features of the underlying probability distribution. The redundant encoding may then rediscover (at least probabilistically) some data which has been scrubbed.

An example of this, consider the following example [from Delip Rao](http://deliprao.com/archives/129). A data set has race scrubbed from it. However, it includes location and income. A second order kernel might then discover `Feature6578 = Loc=EastOakland && Income<10k`. This feature is strongly correlated with race. So although race was scrubbed from the algorithm, this data was redundantly encoded in the data.

One really important thing to recognize is that none of these forms of discrimination necessarily yield *incorrect* results. This means that if gambler A has a gambling strategy based on some sort of discriminatory algorithm, and gambler B has a non-discriminatory one, gambler A might be systematically taking money from gambler B.

**Bias:** This is a statistical property of an algorithm, and there are a variety of fairly technical definitions in different contexts. The most useful one here is that bias is the difference between an estimator's expected value and the true value of a parameter.

## Linear regression

For most of this discussion, I'm going to take linear regression as a toy model.

Linear regression is one of the simplest algorithms for building a predictor. The basic idea is the following. Consider an *output variable* - a quantity I wish to predict. I'm given a set of points:

$$
 (\vec{x}_1, y_1), (\vec{x}_2, y_2), \ldots, (\vec{x}_N, y_N)
$$

The value $@ \vec{x}_i $@ is a d-dimensional vector representing the my input variables. In python terms, it's an array of floats of length d.

The value $@ y_i $@ is a real number which represents my output. In python terms, it's a single float.

Linear regression is the process of coming up with a function of the following form which predicts $@ y_i $@ given $@ \vec{x}_i $@:

$$
y = \vec{\alpha} \cdot \vec{x} + \beta
$$

The vector $@ \vec{\alpha} $@ is another (fixed) d-dimensional vector, and $@ \beta $@ is a scalar. In python terms, we want a predictor of the form:

```python
def y_predict(x):
    assert(len(x) == d)
    result = beta
    for i in range(d):
        result += alpha[i]*x[i]
    return result
```

Using the numpy library for python, one can also simplify this to `return dot(alpha, x) + beta`, but I wrote out the for-loop once for pedagogical purposes.

The goal of linear regression is to find the values of `alpha` (an array of floats) and `beta` (a float) which fit the data as closely as possible, perhaps subject to specific constraints (e.g. sparsity, matching a prior). In this post I'll always be doing least squares fits - choosing $@ \vec{\alpha}, \beta$@ to minimize

$$
\sum_{i=1}^N \left|y_i - \vec{\alpha} \cdot \vec{x}_i - \beta \right|^2
$$

### Pythonic example

Our first example is very simple. We have 3 variables and a true model `alpha_true = [1,2,3]`. We have a data set of 1000 3-dimensional vectors, together with outputs.

The outputs are generated by simply taking the true model and adding random noise to it. In python code:

```python
from numpy import *
from numpy.linalg import lstsq
from scipy.stats import norm

nvars = 3
alpha_true = [1,2,3]

N = 1000

data = norm(0,1).rvs((N, nvars))
output = dot(data, alpha_true) + norm(0,1).rvs(N)

print lstsq(data, output)
```

The output array is:

```
array([ 0.98027674,  2.0033624 ,  3.00109578])
```

This is pretty close to the true value used to generate the input, as it should be.

### Real world example

Suppose we wish to predict first year GPA in college. The variable `x[0]` might represent an SAT [Z-score](https://en.wikipedia.org/wiki/Standard_score) and the variable `x[1]` might represent a high school exit exam Z-score. The variable `y` could represent first year GPA. Then linear regression might yield `x[0] = 0.368` and `x[1] = 0.287` (example is truncated from [here](http://ftp.iza.org/dp8733.pdf)).

So the prediction would be:

$$
\textrm{gpa} = 0.368 (\textrm{SAT z-score}) + 0.287 (\textrm{Exit Exam Z-score}) + \beta
$$

(Here $@ \beta $@ is not directly listed in the paper, but it is a concrete and known value.)

## What if race/other protected class doesn't matter?

Lets consider the following situation. Suppose we want to predict an output variable - say college GPA, following along the example above. Suppose we have two predictive variables - SAT z-score and exit exam Z-score. We also have race as a third variable.

Lets *assume* that for each person, race has no causal relationship with GPA. Suppose we run a linear regression. What will we get? In python terms we've generated the data as follows:

```python
alpha_true = [0.368, 0.287, 0]

N = 1000

data = norm(0,1).rvs((N, nvars))
data = zeros(shape=(N,nvars), dtype=float)
data[:,0:2] = norm(0,1).rvs((N,2)) #Z-score variables
data[:,2] = bernoulli(0.25).rvs(N) #Race, 1 if black

output = dot(data, alpha_true) + norm(0,1).rvs(N)
```

The output is something along the lines of `alpha=[ 0.36679413,  0.32865146,  0.0110941 ]` - we rediscover that SAT and exit exam matter, and race doesn't. Due to statistical noise, the coefficient on race (the third variable) isn't zero, but it's very close. Additionally, there is no particular sign on it - depending on how the noise looks, our predictor might slightly overpredict or underpredict black GPA.

In this case, we have no significant discrimination, no disparate impact, and no redundant coding. We also have no bias.

Most importantly, the algorithm had the opportunity to introduce bias but chose not to. That's hardly surprising; the algorithm's only desire in life is minimizing squared error - being unkind to black people a silly thing that humans seem to enjoy for no apparent reason. If race (or `x[2]` to the algorithm) is not useful in minimizing squared error then the square error minimizer will ignore it, just as Captain Kirk barely noticed the mirror image of the aliens.

Another great essay on distinguishing algorithmic desires from human desires is Bostrom's [parable of the paperclip maximizer](http://www.nickbostrom.com/ethics/ai.html) (see also [lesswrong](https://wiki.lesswrong.com/wiki/Paperclip_maximizer)).

## What if black people don't perform as well?

Now lets consider the following situation. Due to various historical factors, black people perform worse at the pre-college level. At the college level, lets suppose they perform *exactly as well as their pre-college scores predict*. I.e., our causal model changes as follows:

```python
data = norm(0,1).rvs((N, nvars))
data = zeros(shape=(N,nvars), dtype=float)
data[:,0:2] = norm(0,1).rvs((N,2)) #Z-score variables
data[:,2] = bernoulli(0.25).rvs(N) #Race, 1 if black
data[where(data[:,2] == 1),0:2] -= 0.5 # Black people have lower SAT/GPA
alpha_true = [0.368, 0.287, 0] #But holding SAT/GPA fixed, race doesn't matter.

output = dot(data, alpha_true) + norm(0,1).rvs(N)
```

What we are assuming in this case is that race still doesn't matter *holding academics constant*. I.e., a black person with a 1300 SAT is likely to have the same GPA as a white person with a 1300 SAT.

The output? `alpha = [ 0.36904923,  0.29184296,  0.02953688]`. Just like before, we've faithfully reproduced our input model.

However, we've now found a model with a *disparate impact*. The model we have predicts that blacks will score, on average, 0.3278 points lower. The reason the model predicts this is because it's true:

```
In [15]: mean(output[where(data[:,2] == 1)]) #black people
Out [15]: -0.300591159584
In [16]: mean(output[where(data[:,2] == 0)]) #white people
Out [15]: -0.0107252756984
```

So in this case, our model has a disparate impact because it accurately reflects the world. If we want to avoid a disparate impact, the only way we can do that is by adding `+0.30` to the scores of black people, but then we'll be increasing the squared error significantly. We also have no bias.

## What if measurements are biased?

It's been claimed in many places that the SAT, high school GPA, and similar measures are biased against some groups. What would be the effect of this?

Lets suppose we have the following relationship. Each person has an intrinsic `ability`. SAT and high school exit exam are *noisy* measurements of `ability`. Also, lets assume that these measurements are biased - the measurements reduce the scores of black people, but they do not reduce our output variable (namely college performance). Our model looks like this:

```python
ability = norm(0,1).rvs(N) #The true driver

data = norm(0,1).rvs((N, nvars))
data = zeros(shape=(N,nvars), dtype=float)
data[:,2] = bernoulli(0.25).rvs(N) #Race, 1 if black

data[:,0] = 0.5*ability[:] + norm(0,1).rvs(N)
data[:,0] -= 0.5*data[:,2] #Biasing the SAT
data[:,1] = 0.5*ability[:] + norm(0,1).rvs(N)
data[:,1] -=  0.5*data[:,2] #Biasing exit exams

output = ability + norm(0,1).rvs(N)
```

The net result of linear regression here is `alpha = [ 0.34523587,  0.33528078,  0.31779809]`.

Our process in generating the data was biased, but our learning algorithm discovered that and corrected for it!

If we scrubbed the data this result would be impossible. Running least squares on scrubbed data yields `alpha = [ 0.29878373,  0.30869833]` - we can't correct for bias because we don't know the variable being biased on.

As an intellectual exercise, lets consider as a hypothetical that our data was biased differently. Suppose instead of being biased *against* blacks, our measurements were biased in *favor*. The outcome would be more or less the same except that the coefficient on race would be *negative*: `alpha = [ 0.32611793,  0.34397119, -0.30572819]`.

This is pretty cool. Our machine learning algorithm doesn't seem to be doing what the pundits and journalists predict at all. Rather than incorporating human bias, it seems to be detecting it and correcting for it! That's because least squares isn't human. It doesn't know what `data[:,0]` or `data[:,2]` mean - all it knows is that it wants to predict the outcomes as accurately as possible.

So in this example, we have *no disparate impact* and *no bias*. We do, however, have *direct discrimination* - the algorithm is discriminating in favor of blacks in order to cancel out biases earlier in the process.

**Also note:** Under other circumstances, it's totally uncontroversial to claim that a statistical algorithm can eliminate bias. For example, you probably find it completely unsurprising that I can use statistics to [correct for bias in a mobile phone's compass](/blog/2016/bayesian_calibration_of_mobile_phone_compass.html).

### Real world interlude

The analysis above yields some interesting testable predictions. Supposing bias exists, we should be able to detect it by directly conditioning on race and observing the coefficient. If the coefficient is *positive*, it means that the observables are biased against that race. If it's negative, it means they are biased in favor. And if it's zero, it means things are unbiased.

This analysis has actually been done. For example, [this paper](http://ftp.iza.org/dp8733.pdf) discovers that SAT, high school exit exams and similar predictors are mildly biased *against* Asians and fairly strongly in *favor* of blacks. These predictors are also mildly biased against students from high-income families, against women, and in favor of people with unmet educational need.

Similar results [more or less agree with this](http://www.mindingthecampus.org/2010/09/the_underperformance_problem/). Here's a blog post that [links to data](https://randomcriticalanalysis.wordpress.com/2015/05/16/on-concentrated-poverty-and-its-effects-on-academic-outcomes/), so the interested reader can run this analysis themself.

### An alternate formulation of bias

There is a different (but mathematically equivalent) way to formulate bias. Rather than *subtracting* from the input scores, we could equivalently *add* to the output scores.

I.e., we previously chose as our model:

```python
data[:,0] = 0.5*ability[:] + norm(0,1).rvs(N)
data[:,0] -= 0.5*data[:,2] #Biasing the SAT
data[:,1] = 0.5*ability[:] + norm(0,1).rvs(N)
data[:,1] -=  0.5*data[:,2] #Biasing exit exams

output = ability + norm(0,1).rvs(N)
```

What if we instead chose:

```python
data[:,0] = 0.5*ability[:] + norm(0,1).rvs(N)
data[:,1] = 0.5*ability[:] + norm(0,1).rvs(N)

output = ability + norm(0,1).rvs(N)
output += 0.33*data[:,2]
```

The net result is the same - `alpha = [ 0.32258076  0.32353926  0.3253351 ]`. This is a pretty straightforward mathematical equivalence - we are just moving a variable from the left to the right.

This means that we cannot distinguish between the inputs being biased or the factor we are biased on actually being directly causal. I.e., as far as linear regression (and many similar algorithms) is concerned, the propositions "SAT/Exit exams are biased against blacks" is equivalent to the statement "Blacks are 'intrinsically' superior in a manner not reflected in exit exam/SAT". The word 'intrinsically' means that either blackness, or some hidden variable which is correlated with it (the more likely possibility), directly causes outcomes to change.

## What if we scrub race, but redundantly encode it?

Lets now consider the situation where race doesn't matter, and we've scrubbed the data, but we redundantly encode it.

Lets suppose we have 3 new binary variables, generated via the following process:

```python
data[:,2] = race*bernoulli(0.4).rvs(N) + bernoulli(0.1).rvs(N)
data[:,3] = race*bernoulli(0.4).rvs(N) + bernoulli(0.1).rvs(N)
data[:,4] = race*bernoulli(0.4).rvs(N) + bernoulli(0.1).rvs(N)
data[:,2:] = minimum(data[:,2:],1.0)
```

So for each person, we generate 3 new variables, which are either true or false. If a person is black, these variables have a 40% chance of being equal to 1, otherwise they have a 10% chance. This means that the more of these variables are true, the more likely it is that a person is black. The result of regression is `alpha = [ 0.3374577 ,  0.32448367,  0.04370261, -0.01621927, -0.02446477]`.

Even though our algorithm could, if it wanted to, determine a person's race, it has no reason to. This is true even if we include lots of redundant encoding, say 28 of them. The result is simply:

```
alpha = [ 0.33345215,  0.32298627, -0.07885754,  0.00441561,  0.04332198,
          0.00825558, -0.06916433,  0.06032788,  0.02769571, -0.01998633,
          0.06123838,  0.04794704, -0.01579531, -0.00326249, -0.03947687,
          0.00117585, -0.00274476, -0.02228296, -0.02865488, -0.03107947,
         -0.05825314, -0.06108869,  0.03893044, -0.06881212,  0.04479646,
          0.09647968,  0.02672891, -0.04827223,  0.01878823,  0.03254893]
```

In this situation, it's pretty easy to determine if a person is black - compute `sum(data[i,2:])` and check whether it's closer to `0.4*28` or `0.1*28`. If it's the former they are black, if it's the latter they aren't.

The algorithm doesn't care about this redundant encoding because even if it knew, that's not useful. However, if we bias the inputs, suddenly the algorithm does care. Biasing the inputs (as described above) yields `alpha = [ 0.32504926  0.30582667  0.14417805  0.08187899  0.11585452]`.

Equivalently, as discussed above, if race is *directly causal* (which is mathematically equivalent to bias), then the algorithm will also care.

In short, redundant encoding has the same effect (albeit weaker) as directly encoding race. It allows an algorithm to correct for biased inputs or (mathematically equivalently) to discover that one group is intrinsically better/worse performing than another. But that's all it does - discover these effects. It doesn't introduce these effects if they are not present in the data.

*Redundant encoding* does not cause algorithms to vote for Donald Trump. It doesn't make otherwise friendly algorithms wear bedsheets and burn a cross. All it does is give them a piece of data and *allow* them to discover how well that data predicts outcomes. Furthermore, they will only discover the redundant encoding if the data actually matters (very different from what [humans](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3108582/) [do](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0048546))!

## What if you do make statistical errors?

Over at [Algorithmic Fairness](https://algorithmicfairness.wordpress.com/2016/03/15/npr-can-computers-be-racist/), Sorelle points out that sometimes an algorithm doesn't have sufficient training data to actually detect and correct for bias in the manner I've described:

>If an all-white company attempts to use their current employees as training data, i.e., attempts to find future employees who are like their current employees, then they’re likely to continue being an all-white company.

What Sorelle fails to account for is that bias has no consistent sign. Bias like what he describes may exist, but our alien intelligence has no particular reason to give this bias a negative sign. In terms of our analogy above, suppose Captain Kirk jumps to conclusions as to which kind of Cherosian is more dangerous to the Enterprise than the other. Is there any reason for Kirk's bias to be positive towards the Black-Left Cherosian rather than the Black-Right one?

As noted above, in the academic example described, the bias in favor of blacks due to excluding racial data is actually positive! By using a white student body and then doing the linear regression [described here](http://ftp.iza.org/dp8733.pdf) would yield *more* black students, not less. Correcting the bias involves heavily penalizing black applicants; failing to detect the need for this penalty will result in more being admitted. Bias can have a positive sign!

I've seen similar effects in [credit decisions](https://randomcriticalanalysis.wordpress.com/2015/11/22/on-the-relationship-between-negative-home-owner-equity-and-racial-demographics/#my_analysis), though I haven't gone through the details. (I'm a big fan of the randomcriticalanalysis blog because he provides his data.)

Furthermore, this kind of issue falls well within the category of [statisticians not doing their job well](https://www.chrisstucchio.com/blog/2015/dont_use_bandits.html). Algorithms and processes may prematurely converge, but better statistics can prevent this. Fixing the bias is just a matter of running an experiment; allow in enough black students to measure performance in order to get a sufficiently high sample size (due to the $@ n^{-1/2} $@ law, $@ n_w $@ does not have to approach $@ n_b $@).

The key point to takeaway is that bias can have any sign, positive or negative. Alien intelligences might develop bias, but there is no reason whatsoever to expect that their bias will be positive or negative. Sorelle's assumption that alien bias will mimic human bias is nothing but anthropomorphic reasoning.

## Ethical questions

Most of the folks discussing ethical issues surrounding algorithms are, unfortunately, being either innumerate or disingenuous. Machine learning algorithms are not humans in disguise - they are completely alien "intelligences" which think about things in a totally different manner than we do.

![vulcans vs romulans](/blog_media/2016/is_your_algorithm_discriminatory/vulcan_vs_romulan.jpg)

An alien intelligence (human viewers or Captain Kirk) look at the Vulcan and the Romulan above and don't see a big difference. I doubt anyone reading who isn't a Star Trek fan does either. However, over time, Kirk and the viewers learned to tell the difference. Vulcans tend to be peaceful science types like Spock. Romulans tend to be hostile and [destroy Federation outposts](http://memory-alpha.wikia.com/wiki/Balance_of_Terror_(episode)). The prospect of being shot with energy weapons is the only thing that leads an alien intelligence to work hard to distinguish the difference between them - if both were equally hostile or equally peaceful, the viewer would treat their differences like those of the Cheronians.

Machine learning is an alien intelligence. When implemented correctly it will not reproduce human biases; when human biases lead to *factually incorrect* results the alien intelligence will correct them as best it can. Even when given information about factors which bias humans, the alien intelligence will not learn that they matter *unless they do*. Algorithms care about different categories of human as little as dogs, goats or Romulans do.

This leads us to an uncomfortable conclusion. In everyday life we usually assume that racism and stereotypes are *factually incorrect* and driven by human biases; therefore eliminating them we will get better outcomes all around.

When different flavors of intelligence all converge to the same belief, that's evidence that the belief might be true. Intuitively we know and accept this fact. If 10 scientists - each using a different statistical methodology and experiment design - all draw the same conclusion about Gallium Arsenide photonic crystals then we will likely believe them. When 10 data scientists running 20 algorithms draw the same conclusion about humans, we instead call the statistics racist.

We need to start accepting the possibility that discriminatory algorithms might be factually correct and then figure out what to do about it.

The real ethical issues being raised are a lot trickier than what Techcrunch and Mathbabe want to admit. If the issue was simply incorrect algorithms giving wrong conclusions that seem racist, then the solution is simply smarter statisticians with better algorithms. The real ethical issue that the algorithms might be right. Suppose we build a credit allocation algorithm that turns out to be "racist" - i.e., the algorithm accurately predicts that a black person will be more likely to default than a similarly situated white person. Should we ignore this effect, and scrub the model sufficiently in order to eliminate this prediction? That seems like burying our heads in the sand. Is it even beneficial for any individual? Giving a person a loan they are likely to default on seems harmful to both the lender and the borrower, as is admitting a person to a college with a high probability of dropping out.

(I've seen [an analysis](https://randomcriticalanalysis.wordpress.com/2015/11/22/on-the-relationship-between-negative-home-owner-equity-and-racial-demographics/#my_analysis) on the topic of credit but I haven't fully gone through the details. It looks to be in the ballpark of correct, though of course statistics is hard.)

Ultimately there are no easy choices here. It would be wonderful if we had an algorithm which was racially unbiased (neither via direct discrimination nor redundant encoding), accurately predicts college dropouts/delinquent loans/etc, and also serves the needs of "social justice" (a poorly defined term which I understand mainly as mood affiliation). Unfortunately the more we look, the more it seems that we can't have all of these things simultaneously. The ethical question which no one really wants to discuss is what tradeoffs we are willing to make. How many delinquent loans is more individual or group fairness worth?

### My priors

My initial inclination, as of a few years back, was to support race-blind policies - policies which eliminate direct discrimination and *possibly* redundant encoding. Such policies seem intrinsically fair to me. At this point I'm not so sure - the analysis above in the section "What if measurements are biased" suggests this might not be optimal. If we directly include race in a statistical analysis we can accurately correct for existing biases in the input data. This kind of suggests support for traditional affirmative action except that the *sign* is wrong - the most accurate correction we could do (at least for college admissions) would heavily *penalize* blacks and *benefit* Asians (the exact opposite of current policies).

On the other hand, using an algorithm which is directly discriminatory or uses redundant encoding is intrinsically unfair on the level of individuals. I don't like this very much either.

I'm now really confused on the topic.

## Conclusions

Recently, AlphaGo (an AI) played several go matches against Lee Sedol, the champion of the humans. AlphaGo won. Fan Hui, the commentator could only say of AlphaGo's strategy: ["It's not a human move. I've never seen a human play this move"](http://www.wired.com/2016/03/sadness-beauty-watching-googles-ai-play-go/). Earlier this year, an AI was used to [design antennas](https://www.nasa.gov/centers/ames/research/exploringtheuniverse/borg.html). These antennas also don't look like anything a human would have designed. Neither do the laser pulses generated by machine intelligences when [attempting to optimally control quantum state excitation](https://www.ncbi.nlm.nih.gov/pubmed/20151734) - something I studied a little bit in a previous life.

Machine intelligence simply doesn't think the way humans do. When you encounter someone in Techcrunch or NPR assuming machines will reproduce human biases and conclusions, the right question to ask whether those people are clueless or lying to you.
