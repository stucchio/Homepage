title: The Autodidact Ratio: A Better Way to Measure Bias Against Women
date: 2015-12-01 10:00
author: Chris Stucchio
tags: bias detection, frequentist statistics, statistics
mathjax: true

A couple of weeks ago Paul Graham wrote a bit about the detection of bias - i.e., the question of whether a decision process favors some subgroup in a manner that reduces outputs. Specifically, the decision process receives a set of data points and renders a go/no go decision for each one. The goal is to maximize the output of the selected data points. For example, a venture capitalist receives many pitches and attempts to maximize the returns of the portfolio of pitches that they accept.

Graham proposed a bias test, and then I [waded into the fray](/blog/2015/paul_grahams_bias_test.html) to make his results *technically* correct - the best kind of correct. The cool thing about Graham's test is that one could measure whether a decision process is biased *without looking at the inputs*. Graham was interested in whether venture capital is biased against women.

I've also thought a little bit about this issue. In this post I'll discuss a related issue - whether bias at the educational stage prevents some subgroups from entering the technical pipeline. For simplicity I'll refer to men and women, though this could be used to test bias against any two groups relative to each other.

In the debate about women in technology, one of the most troublesome variables is *intrinsic interest and ability* - i.e., the degree to which women may naturally be less capable/interested in technology than men. This is a quantity which is difficult to measure. Furthermore, this variable is *rhetorically* fraught - discussing it's influence causes people to become less rational and more tribal, which of course ends civilized discourse. In this post I'll discuss a way to measure *bias* without actually having to worry about intrinsic interest and ability.

# Are women discouraged/discriminated against in education?

It's well known that considerably fewer women enter the computing workforce than men. The question arises as to why this is. One hypothesis is that various factors in the educational system discriminate against women and discourage them from graduating with technical degrees. If this were true, the net result would be fewer graduating from computing, and therefore fewer entering the workforce via that route.

On the other hand, suppose women simply had a lower innate ability or interest in computing; this would also result in fewer of them graduating from computing.

Lets consider this mathematically. The following Fermi-like equation governs the process:

$$ m_g = m_0 \cdot e_m \cdot a_m $$

$$ w_g = w_0 \cdot e_w \cdot a_w $$

Here, $@ m_g $@ represents the number of male graduates, $@ m_0 $@ represents the number of men in the population, $@ e_m $@ represents the fraction of men who are NOT discouraged by education, and $@ a_m $@ represents the fraction of men with the ability and interest to do computing. The same variables with a w subscript represent these fractions among women.

Concretely, the smaller $@ e_{m/w} $@ is, the more men/women are discouraged by education. And the smaller $@ a_{m/w} $@ is, the less intrinsic ability/interest men/women have.

Unfortunately, looking at the number of graduates doesn't help us answer the question of bias very much. If $@ w_g \ll m_g $@, this could be because either $@ a_w < a_m $@ or $@ e_w < e_m $@. We are completely unable to distinguish between two alternate hypothesis, namely "tech education discriminates against women" and "women have lower intrinsic ability".

Because a large number of ideological people buy into both of these hypothesis, but fiercely disagree with each other, discussion is poisoned. Both groups correctly believe that the data supports them, but fail to recognize it also supports their opponent. What we really need is an alternate measurement which will contradict one of these ideologies (depending of course on the actual value of the measurement).

# The Autodidact Ratio

If we want to tease out the effect of discouragement, we need to find a way to determine what might happen if the discouragement were not present. Fortunately, we have a way to do this - autodidacts!

Autodidacts are people who study computing by themselves rather than in the formal education system. Lets let $@ k_w $@ represent the propensity for a woman with intrinsic ability to learn computing as an autodidact, and $@ k_m $@ for men. Then the number of autodidacts $@ m_g^a $@ is:

$$ m_g^a = m_0 \cdot k_m \cdot a_m $$

$$ w_g^a = w_0 \cdot k_w \cdot a_w $$

Now that we have 4 measurements - the number of male and female graduates, and male/female autodidacts - we can use algebra to eliminate some variables from the equation:

$$
\frac{m_g^a }{m_g} = \frac{ m_0 \cdot k_m \cdot a_m } { m_0 \cdot e_m \cdot a_m } = \frac{ k_m } { e_m }
$$

$$
\frac{w_g^a }{w_g} = \frac{ w_0 \cdot k_w \cdot a_w } { w_0 \cdot e_w \cdot a_w } = \frac{ k_w } { e_w }
$$

The important thing about these equations is that **we no longer need to know the innate ability/interest of men and women**. They depend on two factors - the ability of men and women to learn independently, and the level of discouragement each group has suffered. Innate ability is eliminated from the theory.

So now suppose concretely that $@ w_g^a / w_g $@ were much larger than $@ m_g^a / m_g $@. This would mean one of two things - either $@ k_w > k_m$@, or $@ a_w < a_m $@. I.e., either women are better at learning independently than men, or education hinders women more than it hinders men.

If we assume men and women have equal learning abilities ($@ k_w = k_m $@) - a fairly common assumption - then the only remaining conclusion is that women are more discouraged than men.

# Ideology / Ideology = Truth

Some arguments carry a lot of ideological weight.

Suppose a misogynist internet troll observes someone claiming "tech education is biased against women, you can see this because $@ m_g \gg w_g $@. He can immediately counter argue: "no, women are just dumber than men." This is a very comfortable argument for him to make. His tribalist ideology believes both that the world is not biased against women, and that men are better than women. When the aforementioned troll makes this argument, he is arguing in support of two of his ideological tenets. The social justice warrior makes the counterargument that ability must be equal, and only bias can explain these results. She too is arguing in support of two of her ideological tenets.

Fundamentally the problem is that both ideologies accurately predict the measured value. A theory can only be rejected when it predicts a measurement that does NOT occur.

The autodidact ratio works around this.

Suppose instead that we've observed $@ w_g^a / w_g \gg m_g^a / m_g $@. If troll wishes to argue that this is not due to bias, he can no longer claim the alternate explanation is that women are dumber than men. His new alternate explanation is that *women are better at learning independently than men*; that $@ k_w > k_m $@. If said troll wishes to incorporate this new data point into his worldview, he is forced to give up one of his ideological tenets - either the world is biased against women **or** men are intellectually superior to women.

Conversely, suppose we discover that $@ w_g^a / w_g \approx m_g^a / m_g $@. The social justice warrior who wishes to argue that bias still exists must then immediately argue that women are *not intellectually equal to men.* If the ratios are equal, and $@ a_w = (1/2) a_m $@ for example, then $@ k_w = (1/2) k_m $@. In much the same way as the internet troll above, the social justice warrior must give up one of her ideological points.

Because we've put ideology in both the numerator and the denominator, ideology cancels and we may learn something new.

# A measurement is only fun if it can change your beliefs

I strongly discourage my readers from googling data on autodidacts, at least to start with. A useful intellectual exercise is to consider the two hypotheticals above and decide how your beliefs will change after such a measurement.

My current belief (I have not found any data on this) is that it is unlikely that education is significantly biased against women. I also believe that autodidact ability is roughly equal, and may skew slightly in favor of men. Therefore if I see data showing that $@ w_g^a / w_g \gg m_g^a / m_g $@, I'll change my beliefs and conclude that the tech educational system is biased against women.
