title: Python LRU Cache version 0.1.1 released
date: 2014-11-01 10:00
author: Chris Stucchio
nolinkback: true
tags: python, caching, development

I've just released a [new version](https://pypi.python.org/pypi/py_lru_cache) of my Python LRU Cache library. Source code is available [on github](https://github.com/stucchio/Python-LRU-cache).

The new version of the library allows you to evict keys from the cache using a daemon thread. Previous versions would only evict whenever a method was called on the cache. As a result, long term control over memory usage can be improved. This is helpful for me, because for my automated trading program, the objects contained in the cache are very often largish dataframes.

Concurrent cache eviction is triggered as follows:

```python
import lru
cache = lru.LRUCacheDict(expiration=30, thread_clear=True, thread_clear_min_check=10)
```

This will create a cache which will have a delay of no more than 10 seconds between cache evictions.

You can also create a thread safe cache with the `concurrent` argument:

```python
thread_safe_cache = lru.LRUCacheDict(concurrent=True)
```
