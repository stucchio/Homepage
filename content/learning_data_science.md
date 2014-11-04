title: Bibliography for learning statistics/data science (mostly free)
date: 2014-11-20 00:00
author: Chris Stucchio
tags: data science, statistics
category: statistics

A lot of people ask me how to get started learning statistics. Unfortunately, I've never been able to offer good suggestions, since the path by which I arrived here has been rather circuitous. If you want to do statistics, I do NOT recommend first learning quantum mechanics, then Bohmian mechanics, and finally Bayesian statistics.

But over time, I've cooked up what I think is a fairly straightforward trajectory. The trajectory I'm going to describe strongly emphasizes understanding the mathematics. I take the perspective that statistics/data science is a fundamentally mathematical practice, and merely implementing the algorithms without understanding them is destined to be a pointless exercise.

# Step 1: The basics

## 1M) The mathematical front

There are two major mathematical foundations for everything else one might do in statistics and data science. These foundations are the theory of integration and linear algebra, and can be learned from any undergraduate calculus and linear algebra textbook.

The standard linear algebra text is [Linear Algebra, by Hoffman and Kunze](http://www.amazon.com/gp/product/0135367972/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=0135367972&linkCode=as2&tag=christuc-20&linkId=EPPJGRIKX54BJGLJ), but there are probably many other books which are equivalently good. The version I linked to is $150, but [cheaper versions are available](http://www.amazon.com/gp/product/8120302702/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=8120302702&linkCode=as2&tag=christuc-20&linkId=2ZRECLN7FH3B44F2). The goal of learning linear algebra is to understand the concept of vectors, linear transformations, and their representation as a list of numbers.

## 1A) The algorithmic front

At this stage you should also try to gain a concrete understanding of standard algorithms. There are two relatively standard texts on this topic; [Introduction to Algorithms](http://www.amazon.com/gp/product/0262033844/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=christuc-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=0262033844) by Cormen and the [Algorithm Design Manual](http://www.amazon.com/gp/product/1849967202/ref=as_li_ss_tl?ie=UTF8&tag=christuc-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=1849967202) by Skiena. The latter book is a bit more elementary.

# Step 2: More basics

## The mathematical front

The next step in learning the basics is [Foundations of Data Science](http://www.cs.cornell.edu/jeh/NOSOLUTIONS90413.pdf) by John Hopcroft. Luckily this book is free and superior to anything else I've seen out there. The book starts off by discussing high dimensional vector spaces and their geometry. This chapter alone is excellent - it explicitly states and proves a variety of facts which are implicitly used by many learning algorithms.

It then discusses random graphs, a vitally important topic. It moves on to singular value decompositions, a widely used technique in linear algebra which is underappreciated in mathematics. Markov chains are also covered, and finally it moves into traditional data science topics like VC dimension, linear separators, clustering and the like.

I recommend reading this book because you will gain an intuitive understanding of why the various learning algorithms work and what they are trying to compute.

Most of the mathematics is elementary. If you've gained a solid understanding of the theory of integration from Step 1, you'll be able to follow the proofs in this book. It will take effort, but it will be well worth it.

## The algorithmic front

Once you have a grasp on the algorithms from step (1A), a good text to move forward is [Mining of Massive Data Sets](http://infolab.stanford.edu/~ullman/mmds/book.pdf) by Leskovec, Rajaraman and Ullman. This book focuses on the details of applying an algorithm to a dataset too large to fit into the memory of a single computer.

At this stage I'd also suggest learning a "small data framework" such as Matlab, Mathematica, R or Python/Numpy/Scipy. I personally prefer and recommend the Python stack since it's free software (ruling out Matlab/Mathematica) and since it's a better general purpose language than R.

# Step 3: Details

[Probabilistic Graphical Models](href="http://www.amazon.com/gp/product/0262013193/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=0262013193&linkCode=as2&tag=christuc-20&linkId=73DQJUHLUQY6XCNP) by Koller and Friedman is the standard introduction for inference networks.
