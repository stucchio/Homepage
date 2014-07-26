title: Bounded Rationality and the Ellsberg Paradox
date: 2014-07-24 21:00
author: Chris Stucchio
tags: probability, bayesian reasoning, utility functions, rationality
mathjax: true

The [Ellsberg paradox](http://en.wikipedia.org/wiki/Ellsberg_paradox) is a puzzle concerning human rationality. It postulates a scenario involving an urn with 90 balls inside - 30 red ones, while the remaining 60 can be yellow or black. A player gets to draw a ball from the urn, and receives a payoff dependent on the color. The player is then given options for various bets. In practice, humans are shown to display *inconsistent* preferences as to which bets are worth taking - this is completely irrational behavior under any reasonable theory of probability. In this post I'll ponder this question, and postulate a model of bounded rationality characterized by "problem boundaries" which may shed some light on this puzzle.

# The Ellsberg Paradox

The Ellsberg paradox consists of the following situation. An urn contains 90 balls - 30 red, and the remainder are yellow and black. Let us denote by $@ n_y $@ and $@ n_b $@ the number of yellow and black balls.

The player is offered two potential gambles:

- **A1** Draw a ball. If the ball is red, the player receives $100.
- **A2** Draw a ball. If the ball is black, the player receives $100.

The player is then offered two alternative gambles:

- **B1** Draw a ball. If the ball is red or yellow, the player receives $100.
- **B2** Draw a ball. If the ball is black or yellow, the player receives $100.

Lets work this out mathematically. The expected payout of these bets is:

- **A1** The payoff is $@ $100 \cdot 30 / 90 = $33 $@
- **A2** The payoff is $@ $100 \cdot n_b / 90  $@.
- **B1** The payoff is $@ $100 \cdot (30+n_y)/90 $@
- **B2** The payoff is $@ $100 \cdot (n_b + n_y)/90 = $100 \cdot 60/90 = $66 $@

From these formulae, we can draw the following conclusions. Suppose the player considers **A1** better than **A2**. This means that $@ n_b < 30 $@, and hence $@ n_y = 60 - n_b > 30 $@. From this, we can conclude that if the player considers **A1** better than **A2**, they must believe that $@ 30 + n_y > 30+30$@, and thus **B1** must be better than **B2**.

In real life, people tend to prefer option **A1** over **A2** and option **B2** over **B1**, contradicting the laws of arithmetic.

# Bounded Rationality

The theory of [Bounded Rationality](http://en.wikipedia.org/wiki/Bounded_rationality) supposes that the ability of humans to reason rationally is bounded - for whatever reason, humans are incapable of thinking through every possibility.

I propose one possible mechanism for this. It's based on the concept of [variable scope](http://en.wikipedia.org/wiki/Scope_(computer_science)) in computer science.

Specifically, I suppose that each subproblem is solved in it's own subroutine. The routine for solving A (i.e., determining whether A1 is better or worse than A2) looks like this:

```scala
def solveA = {
    nb_guess <- chooseConservatively
    payoff_a1 = 100.0 * 30 / 90.0
    payoff_a2 = 100.0 * nb_guess / 90.0
    if (payoff_a1 > payoff_a2) {
        return "choose A1"
    } else {
        return "choose A2"
    }
}
```

The function `chooseConservatively` is an oracle function which chooses `nb_guess` in some sense "conservatively" to avoid the risk of losing too much *for the current problem only*.

The routine for solving problem B looks like this:

```scala
def solveB = {
    ny_guess <- chooseConservatively
    payoff_b1 = 100.0 * (30+ny_guess) / 90
    payoff_b2 = 100.0 * 60 / 90
    if (payoff_b1 > payoff_b2) {
        return "choose B1"
    } else {
        return "choose B2"
    }
}
```

The key part of the theory is at the end of the lexical scope (i.e., the last `}`), the intermediate variables vanish. So *during* the execution of `solveA`, the value of `nb_guess` is available. Once the solution is computed, and the `return ...` statement is reached, the intermediate variables (namely `nb_guess`, `payoff_a1` and `payoff_a2`) exit the local scope and are lost.

Because of this, there can be no relation between `nb_guess` and `ny_guess`. This allows `nb_guess` to pessimistically estimate the payoff probability in problem A, while `ny_guess` pessimistically estimates the payoff probability in problem B.
