Is white nationalism a serious problem? Extracting wikipedia data with Python.
##############################################################################
:date: 2019-03-21 08:30
:author: Chris Stucchio
:tags: terrorism, python


I recently saw a `silly twitter exchange <https://twitter.com/AOC/status/1107757871477985280>`_ between two of the lyingest politicians in American politics. Given that they have both explicitly expressed the viewpoint that morals matter more than numbers and being "technically correct", I figured that I should use python to answer the question of whether white supremacists are a serious problem worldwide. In the silly twitter exchange, Trump says it's a small group of people with serious problems while Alexandria O. Cortez claims "White supremacists committed the largest # of extremist killings in 2017". This question is easily answerable.

So actually no, this blog isn't about politics. But I recently discovered `pandas.read_html`, and two idiot politicianss tweeting at each other is as good as reason as any to write a blog post about it. The real audience for this post is python developers who want to see a couple of cool pydata tricks I've learned recently.

Cool python trick #1: `pandas.read_html`
----------------------------------------

This is one of the coolest tricks I've learned in 2019. The `pandas` library has a method, `read_html <http://pandas.pydata.org/pandas-docs/version/0.19.2/generated/pandas.read_html.html>`_ which takes a webpage as input and returns a list of dataframes containing the tables on that webpage.

So to answer the question about terrorism in 2017, I'm going to browse Wikipedia's `List of Terrorist Incidents in 2017 <https://en.wikipedia.org/wiki/List_of_terrorist_incidents_in_2017>`_.

Sadly, there's a lot of terror attacks, so they have separate pages for each month. Each page looks like this: `https://en.wikipedia.org/wiki/List_of_terrorist_incidents_in_January_2017 <https://en.wikipedia.org/wiki/List_of_terrorist_incidents_in_January_2017>`_.

Therefore, to extract the data I'll do this::

    import pandas
    def load_month(m):
        results = pandas.read_html('https://en.wikipedia.org/wiki/List_of_terrorist_incidents_in_' + m + '_2017')
        df = results[0]
        df.columns = df[0:1].values[0]
        return df[1:].copy()
    data = []
    for month in [datetime(2008, i, 1).strftime('%B') for i in range(1,13)]:
        data.append(load_month(month))
    data = pandas.concat(data)

The function `read_html` is doing all the heavy lifting here.

The result of this is a dataframe listing a location, a perpetrator, a number of deaths/injuries, and a few more columns. It's not super clean, but at least it's pretty structured.

This `read_html` function is awesome because I needed to do literally no work parsing.

Cool python trick #2: the `wikipedia` module
--------------------------------------------

In this data, there were 230 separate perpetrators listed *after* cleaning up some of the obvious data issues (e.g. some rows containing `Al Shabaab` and others containing `Al-Shabaab`). That's far too much for me to manually classify everything.

So instead I used the `wikipedia` module.::

    import wikipedia

    def get_summary(x):
        if x == 'Unknown':
            return None
        try:
            return wikipedia.page(x).summary
        except Exception:
            return None

    count['perp_summary'] = count['perpetrator_cleaned'].apply(get_summary)

This gets me a summary of each terrorist group, assuming wikipedia can easily find it. For example, here's the result of `get_summary('Al-shabaab')`:

    'Harakat al-Shabaab al-Mujahideen, more commonly known as al-Shabaab (lit. \'"The Youth" or "The Youngsters", but can be translated as "The Guys"\'), is a jihadist fundamentalist group based in East Africa. In 2012, it pledged allegiance to the militant Islamist organization Al-Qaeda.[...a bunch more...]

With a little bit of string matching (e.g. if the summary contains "Communist" or "Marxist", classify as "Communist"), I was able to classify assorted terrorist attacks into a few broad causes::

    cause                       dead
    Islam                       8170.0
    Central Africal Republic    432.0
    Communism                   310.0
    Myanmar                     105.0
    Congo                       85.0
    Anarchy                     3.0
    Far-right                   3.0
    Far-left                    1.0

Some of these are broad catch-all terms that simply reflect my ignorance. For example, one group is called `Anti-Balaka <https://en.wikipedia.org/wiki/Anti-balaka>`_, and wikipedia explains them as a predominantly Christian rebel group "anti-balakas are therefore the bearers of grigris meant to stop Kalashnikov bullets". I lumped a bunch of similar groups into "Central African Republic", similarly for "Congo" and "Myanmar".

This classification scheme let me classify 92% of the 9933 deaths due to terrorism. Note that Islam alone accounted for at least 82%, and eyeballing the groups I didn't match it's probably higher.

There were also a number of attacks that I found very hard to classify, e.g. `Patani independence <https://en.wikipedia.org/wiki/Barisan_Revolusi_Nasional>`_ or `Fulani pastoralism <https://buzznigeria.com/fulani-herdsmen-attack/>`_. Key summary of the Fulani Pastoralism conflict: the Fulani people of Nigeria are mostly nomadic cow herders and they are getting into violent land disputes with non-Fulani farmers who don't want Fulani cows eating/trampling their crops. The world is a big place and it's full of all sorts of bad shit most folks have never heard of.

Conclusion
----------

It looks like Donald Trump is right and AOC is wrong. Even if we take high end estimates of the number of people killed by white supremacists in 2017 (34 in the US according to the SPLC), it seems like a small problem compared to things like Anti-Balaka, Communism or `Balochistan independence <https://en.wikipedia.org/wiki/Insurgency_in_Balochistan>`_.

There are many individual terrorist groups that I imagine most readers have never heard of, such as Indian Naxalites (communists), which kill far more people than white supremacists.

Also, far more importantly for most of my readers, you can easily extract data from Wikipedia into a dataframe using `pandas.read_html` and the `wikipedia` module.

Methodology
-----------

You can find my python notebook `here </blog_media/2019/python_and_terrorism/Untitled1.ipynb>`_.

**Correction:** A previous version of this post described an "Independent Nasserite Movement (a Socialist pan-Arab nationalist movement)", which was a reference to `Al Mourabitoun <https://en.wikipedia.org/wiki/Al-Mourabitoun>`_. However that might have been me getting confused by wikipedia results - I think the actual attack in 2017 was done by a different `Al Mourabitoun <https://en.wikipedia.org/wiki/Al-Mourabitoun_(militant_group)>`_ which is just ordinary boring Islamist violence. So we probably need to add another 77 or so to the Islam row.

**Also**, at least one commenter noted that the SPLC counts 34 dead due to white nationalists, which is higher than I get from Wikipedia. I don't particularly trust the SPLC, but I do reference it above. It still doesn't really change the results. Fulani Pastoralism killed more people.
