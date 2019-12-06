Backtest your SQL queries - they are models too
###############################################
:date: 2019-12-15 08:30
:author: Chris Stucchio
:tags: data science, sql, programming


I was recently discussing a project with a younger data scientist and I noticed a curious mismatch between our language. We had an API that we wanted to impose rate limits on. We want to ensure that 99% of our good customers have a good experience and never hit the rate limit, while locking down the heaviest users to prevent overload. We also want to limit the potential damage caused by malicious usage.

Luckily all usage was nicely logged in redshift. For simplicity, lets assume we have a table ``endpoint_usage`` with columns ``endpoint_url``, ``user_id``, ``daily_requests``, ``date`` and ``malicious``. The ``malicious`` flag is an indication of malicious usage of the API, and is unfortunately not something which can be computed in realtime. (If we could compute it in realtime, then we could simply use this flag instead of a rate limit.)

Our analysis was therefore quite simple - we'll just measure the historical usage of our bottom 99% of non-malicious customers and use that. The code was not much more sophisticated than this::

  SELECT endpoint_url,
         PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY daily_requests) OVER (PARTITION BY endpoint_url) AS num_requests_99pct
    FROM endpoint_usage
      WHERE (NOT malicious)
    GROUP BY endpoint_url

We are excluding malicious users from this query because we do not care about keeping them happy.

The SQL is complex, but what it's doing is computing the 99'th percentile of ``daily_requests`` over each ``endpoint_url``. Unfortunately Postgres/Redshift do not have a ``PERCENTILE`` aggregate function. Only a window function is provided and the syntax for window functions is a bit more complex. If we were taking the 100'th percentile (i.e. ``MAX``) instead of the 99'th, it would simply be::

   SELECT endpoint_url, MAX(daily_requests)
    FROM endpoint_usage
      WHERE (NOT malicious)
    GROUP BY endpoint_url

Those of you who know what I do know I'm actually not rate limiting an API, but instead allocating capital and choosing bet sizes for real money gambles. But those are trade secrets so I'll stick to this example.


Me: "Is the rate limit model ready to go?"

Her: "You mean running the rate limit SQL query on a cron job?"

Me: "Yes, but also are we backtesting the model?"

Her: "What do you mean 'model'? It's just a SQL query."

Me: ...gave explanation that makes up the rest of this blog post...

To be very clear, I am not attempting to dress up a SQL query as something more sophisticated than it is. I am not a big fan of the hype train that turns simple linear regression into "AI".

Nevertheless, I believe that concepts made popular in data science are valuable even for simple programming tasks such as this.


Big Idea: Your Analysis is a Model
==================================

Fundamentally a model is code that attempts to predict the future. Unfortunately, predicting the future is hard, so we need to be very careful about doing it.

The analysis being performed above is quite simple. The most obvious way to do it would be to simply open up Jupyter, run the analysis once, and then hardcode the result into the production system. Most product managers would be very happy with this.

But ultimately, we aren't doing a historical analysis. Our goal is to rate limit the API in such a way as to minimize the impact on *future* non-malicious users. We are attempting to predict the future, specifically future usage of the API.

We're making an implicit modeling assumption here that should be made explicit: past usage and future usage are very similar.

Just like any other data science model, our predictions might be wrong (or at least less right than we think).


All models should be backtested
-------------------------------

To backtest a model is to simulate what *would have* happened had we used the model in the past.

Let's be concrete. Suppose we plan to train this model monthly. It's currently December so we have a complete month of data from November. Therefore, we'll calculate thresholds *for November* as follows::

  SELECT endpoint_url,
         PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY daily_requests) OVER (PARTITION BY endpoint_url) AS num_requests_99pct
    FROM endpoint_usage
      WHERE (NOT malicious)
            AND (date < '2019-11-01')  -- This part is new
    GROUP BY endpoint_url

This tells us what the rate limits *would have been* during the month of November if we ran this code on Nov 1.

Then we'll measure what fraction of non-malicious users would have gotten rate limited during the month of Nov. In this query, the ``rate_limits`` table is a temporary table generated from the output of the above (i.e. ``(date < '2019-11-01')``) query::

  SELECT endpoint_url, COUNT(*) AS total_usage,
         SUM(CASE WHEN (daily_requests > num_requests_99pct) THEN 1 ELSE 0) AS num_rate_limited,
    FROM endpoint_usage
      INNER JOIN rate_limits ON (endpoint_usage.endpoint_url = rate_limits.endpoint_url)
    WHERE (NOT malicious)
          AND (date >= '2019-11-01') AND (date < '2019-12-01')
    GROUP BY endpoint_url

This query tells us the total usage as well as the total fraction of usage that gets rate limited. Concretely, a single user who uses the API for 5 days and got rate limited once would contribute 5 to ``total_usage`` and 1 to ``num_rate_limited``.

If ``num_rate_limited`` is 1% of ``total_usage``, we're in business! Our modeling assumption appears to be true and we can safely put this model into production.

If it's not, then we might need to do more work.


Does the model change over time?
--------------------------------

Most ML models do not retain their accuracy indefinitely. In this case, it is worth considering the possibility that legitimate API usage might change over time. So we might wish to train our model over a shorter time period. Then we would periodically update our bet sizes.

Of course, if we do this, we also need to test the results and see if affects the accuracy of the model.


Putting it into production
==========================

Instead of simply running this SQL query once and hard coding the result, we can have a much more robust system with a moderate amount of effort. We'll follow the exact same steps as putting a data science model into production:

1. Set up a cron job (or better, an `Airflow dag <https://airflow.apache.org/>`_ to run the query (i.e. train the model) every month.
2. Set up a second cron job to run the backtest every month. This means that on Jan 1, the code should generate rate limits using data available up to Dec 1. Then it should check how many users exceeded those rate limits during Dec 1-Dec 31. The results of this should be posted to a slack channel, a dashboard, or some other regularly monitored location.
3. Ensure proper alerting. If the API usage in redshift drops below some expected level, raise an alert - the model might be broken due to insufficient data (or data collection might simply be broken). If the number of non-malicious users getting rate limited exceeds an expected threshold (e.g. 3-5%), similarly an alert should be raised. Models are finicky things and you should not skimp on the sanity checks.

(Obviously adjust "monthly" to whatever makes sense for your use case.)

Ultimately, the idea of running a train/test split on historical data and auto-update your parameters is a very powerful paradigm. It is normally applied to complex data science models (think: gradient boosting, neural networks), but even many simple tasks can benefit from this process as well.
