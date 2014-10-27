title: A simple trick to speed up complex Postgres queries on EC2
date: 2011-12-12 00:00
author: Chris Stucchio
tags: ec2




A major problem with running Postgres on EC2 is that EBS performance often sucks. In addition to performing poorly, EBS also uses the network connection, which can be undesirable. Ephemeral storage is provided, and tends to have better performance characteristics, but unfortunately it lacks durability.


However, we can still use it to speed up Postgres on complex queries. Postgresql has a concept called [tablespaces](http://www.postgresql.org/docs/9.1/static/manage-ag-tablespaces.html) - a tablespace is basically a location in the filesystem where postgres objects can be stored.

In particular, postgres has the [temp_tablespaces](http://www.postgresql.org/docs/9.1/static/runtime-config-client.html#GUC-TEMP-TABLESPACES) configuration setting. This setting determines which tablespace postgres will use to store temporary tables, which are often created during complex queries.

So here is how we speed up postgres - we move the temporary tablespace to ephemeral storage. This is safe, since no data is permanently stored in the temporary tablespace.

    #!sql
    psql&gt; CREATE TABLESPACE ephemeral LOCATION \'/mnt/postgresql_tmp\';

We then modify postgresql.conf to tell postgres to use this tablespace for temporary objects:

    #!conf
    temp_tablespaces = 'ephemeral'

Finally, restart postgres.

For some of my complex queries (involving 4 joins), this gives a 30% improvement in speed and cuts network usage by about half.


