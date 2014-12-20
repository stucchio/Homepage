title: Monads are like a dildo factory, staffed by midgets
date: 2013-06-11 08:24
author: Chris Stucchio
tags: algorithms, monads





At their most basic, monads are a monoid in the category of endofunctors. But that's an explanation that only appears to mathematicians. They are also a design pattern, but that's an explanation that only appeals to computer geeks.

You've read many [monad tutorials](http://www.haskell.org/haskellwiki/Monad_tutorials_timeline). For instance, [monads are like monsters](http://www.haskell.org/pipermail/haskell-cafe/2006-November/019190.html). No wait, monads are like space suits, and functions of type `a -> M b` are like space brothels where you take off your suit, get space herpes and then put your suit back on. But this post is the ultimate in monad tutorials - this is the one that will finally cause them to make sense in your mind.

So consider a program being used to run a dildo factory. The most basic underlying type is the `Dildo`:

    data Dildo = NormalDildo | Rabbit | StrapOn | ...

We also have a data type representing the box:

    data Box a = Box a

Now consider one of the midgets, who's job it is to do work to a dildo and put it into a box. In the abstract, the type signature of the midget is `Dildo -> Box Dildo`. But sometimes the midgets need to take a dildo out of the box, do some work on it, and put it back into the box. Monads to the rescue.




**Stop reading fucking monad tutorials and write some code**

You didn't learn python via abstract tutorial, comparing lists to Smaug and dicts to Bilbo. You learned it by writing some fucking code. You won't learn Haskell or Scala any other way. This is true even if you are a hotshot hipster brogrammer who knows PhP, Ruby *and* node.js.

STFU and code. There is no other way to learn to code.

**Note:** If you found this blog post via google while looking for something *completely different*, maybe [this](http://www.amazon.com/gp/product/B00BON42WO/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00BON42WO&linkCode=as2&tag=christuc33-20) or [this](http://www.amazon.com/gp/product/B00A27H3VA/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00A27H3VA&linkCode=as2&tag=christuc33-20) is what you are looking for.
