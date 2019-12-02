Treat your SQL Query like a Data Science Model
##############################################
:date: 2019-12-15 08:30
:author: Chris Stucchio
:tags: data science, sql, programming


I was recently discussing a project with a younger data scientist and I noticed a curious mismatch between our language. We were attempting to allocate funding to a sequence of gambles; our goal was to minimize funding allocation while covering 90% of our winning bets. Our analysis was quite simple - we'll just measure the historical amount needed to cover 90% of the bets and use that. The code was not much more sophisticated than this::

  SELECT game_id, actual_bet_size, max_bet_size
         PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY actual_bet_size) OVER (PARTITION BY game_id) AS bet_size_90pct
    FROM gambles
    WHERE (gambles.outcome = TRUE) AND
         (max_bet_size > {threshold})

In python/pandas, it might look like this (assuming `df` is properly filtered, as per the positive outcome and sufficient max bet size conditions above)::

  df.groupby('game_id').agg(lambda x: np.percentile(bet_size, 90))


Me: "Lets build a max-bet model just like your min-bet model."

Her: "You mean run a similar query for the maximum bet size?"

Me: "Yes, but in this case lets evaluate the model more carefully."

Her: "What do you mean model? It's just a SQL query."


To be very clear, I am not attempting to dress up a SQL query as something more sophisticated than it is. I am not a big fan of the hype train that turns simple linear regression into "AI".

Nevertheless, I believe that concepts made more popular in data science have a valuable even for simple programming tasks such as this.

Big Idea: Your Analysis is a Model
==================================

The analysis being performed above is quite simple. A straightforward way to solve the problem is to simply open up Jupyter, run the analysis once, and then hardcode the result into the production system. Sounds good, right?

Unlike a random forest or deep neural network, the model in this case is quite simple: a hash table mapping `game_id` to the 90'th percentile. There's no need for any particularly fancy serialization; you could easily store the result as a CSV or parquet file and check it into git.

But this query result faces all the same pitfalls as any ML method.

Does the model generalize?
--------------------------

The goal of this outcome is to allocate enough funding to cover 90% of gambles. So the important step when building any model is to evaluate the model on an out-of-sample test. This can be done fairly straightforwardly::

  SELECT game_id, actual_bet_size, max_bet_size,
         PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY actual_bet_size) OVER (PARTITION BY game_id) AS bet_size_90pct
    FROM gambles
    WHERE (gambles.outcome = TRUE) AND
         (max_bet_size > {threshold}) AND
         (gambles.timestamp < {cutoff_date})  -- This part is new

Note that we've added the term `(gambles.timestamp < {cutoff_date})` to the `WHERE` clause. The time `{cutoff_date}` is a healthy distance in the past - perhaps 3 months. This data set tells us the max bet sizes we'd have allowed if we ran this query 3 months ago.

Then we would pull the following data set, the out-of-time data set::

  SELECT game_id, actual_bet_size, max_bet_size
         PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY actual_bet_size) OVER (PARTITION BY game_id) AS bet_size_90pct
    FROM gambles
    WHERE (gambles.outcome = TRUE) AND
         (max_bet_size > {threshold}) AND
         (gambles.timestamp >= {cutoff_date})  -- This part is new

This is the actual gambling data over the most recent 3 months.

Once we've pulled this data set we want to check if the thresholds we would have calculated 3 months ago would have *actually* allowed us to cover 90% of our bets today. If so, great - it seems like we've found a model with predictive power.

Does the model change over time?
--------------------------------

Most ML models do not retain their accuracy indefinitely. In this case, it is worth considering the possibility that bet size might change over time. So we might wish to train our model over a shorter time period: `(gambles.timestamp < {cutoff_date}) AND (DATEADD(month, 1, {cutoff_date}) < gambles.timestamp)`

Then we would periodically update our bet sizes.


To summarize
============

Instead of simply running this SQL query once and hard coding the result, we can have a much more robust system with a moderate amount of effort. We'll follow the exact same steps as putting a data science model into production:

1. Set up a cron job to run the query (i.e. train the model) every month based on 3 month old data.
2. Test whether or not predictions of 3 month old data work adequately on the most recent 3 months of data. Post the result of this to a slack channel for monitoring.
3. Have a second cron job run the query every month based on the most recent data. Use this to make predictions in production.

Ultimately, the idea of running a train/test split on historical data and auto-update your parameters is a very powerful paradigm. It is normally applied to complex data science models (think: gradient boosting, neural networks), but even many simple tasks can benefit from this process.
