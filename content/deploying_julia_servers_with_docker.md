title: Deploying Julia Servers with Docker
date: 2014-11-11 09:00
author: Chris Stucchio
tags: julia, docker

As a result of a new work project, I've now gotten the opportunity to use Julia in anger. The first part of the project was a standard Julia task - a purely scientific R&D project, culminating in a command line script. The problem involves deriving algebraic constraints on a business process and then using convex optimization in order to optimize that process. Overall, this is fairly standard operations research, merely applied to a new domain.

But the second part of the project is where things get interesting. Rather than simply delivering the command line script, it's necessary to package it and build a deployable version. Nothing fancy, just a little json-over-http endpoint that connects to a database. Time to put Julia to the test.

At the moment, Julia is *not* a particularly good language for building CRUD-type apps. In principle there is nothing that should prevent it from being used for this purpose, but the infrastructure, knowledge and libraries aren't there. Since I've found very little information on the web as to how this is done, I've decided to write up my experiences. Consider this blog post a set of notes explaining how I made it work, not a set of best practices.

# Julia Packages

The first issue with building a deployable app is that Julia simply lacks a virtualenv. In fact, most of Julia's [package management system](http://julia.readthedocs.org/en/latest/manual/packages/) seems designed around building libraries that you install on your desktop and use for interactive sessions. There are two main methods for installing libraries - in the console, via `Pkg.add("mylib")`, or by adding entries to the *global* `REQUIRE` file.

Unlike Python, there is no equivalent of creating an application-specific `requirements.txt` file and then running `pip install -r requirements.txt`. One can, however, create *library* specific `REQUIRE` files which specify their dependencies.

The second issue with Julia packaging is that a lot of what you need to build a Julia program are C libraries - unfortunately, Julia's package management system does not handle this at all. Fortunately, such libraries can usually be installed in a fairly straightforward way with the operating system's package manager.

# Docker images

The first thing we'll do is create a base Julia docker image:

```
FROM ubuntu:14.04
MAINTAINER Chris Stucchio <stucchio@gmail.com>

# Necessary to add a ppa
RUN apt-get update && apt-get install -y python-software-properties software-properties-common

# Julia repository
RUN add-apt-repository ppa:staticfloat/juliareleases && apt-get update

# Yay julia
RUN apt-get install -y julia
# Ensure existence of base julia package folder
RUN julia -e "Pkg.resolve()"
```

We then build the image with `$ sudo docker build -t stucchio/juliabase:0.3.2 .`.

We create a second docker image for the web stack:

```
FROM stucchio/juliabase:0.3.2
MAINTAINER Chris Stucchio <stucchio@gmail.com>

# C Libraries we need
RUN apt-get install -y libhttp-parser2.1 libicu52 # Utility libs for parsing unicode and http
RUN apt-get install -y libpq # For postgresql
RUN apt-get install -y unixodbc unixodbc-dev odbc-postgresql # Needed if we want to use ODBC

# Julia libs we want
ADD REQUIRE /.julia/v0.3/REQUIRE
RUN julia -e "Pkg.resolve()"

# Julia libraries which are not published
RUN julia -e 'Pkg.clone("https://github.com/JuliaDB/DBI.jl.git")' && julia -e 'Pkg.clone("https://github.com/iamed2/PostgreSQL.jl.git")'

```

The file `REQUIRE` should be located in the same folder as this Dockerfile, and should list the required julia libraries. Note the last line which is necessary to install *unpublished* packages in Julia. My require contains:

```
NamedArrays
DataStructures
ODBC
HttpServer
HttpParser
HttpCommon
Morsel
Meddle
```

# Database access

There seem to be two major ways to access a database with Julia. One is the [ODBC.jl](https://github.com/quinnj/ODBC.jl) library, which is a wrapper around Microsoft ODBC. From what I can tell, ODBC is a Microsoft written C-language version of JDBC. This is the recommended way to connect according to a few google searches. Unfortunately I was not able to make ODBC connect to Postgres.

The other way is with [DBI.jl](https://github.com/JuliaDB/DBI.jl) and [PostgreSQL.jl](https://github.com/iamed2/PostgreSQL.jl). These libraries work like a charm for me. These libraries are not actually published packages, so to add them one will need to clone them directly from github.

To add them to the docker container, I add this to the web stack dockerfile:

```
RUN julia -e 'Pkg.clone("https://github.com/JuliaDB/DBI.jl.git")' && julia -e 'Pkg.clone("https://github.com/iamed2/PostgreSQL.jl.git")'
```

In development I'm using the official [postgres docker image](https://registry.hub.docker.com/_/postgres/). So I'll connect to that using docker linking. That means I can spin up a development environment as follows:
```shell
# Run the postgres docker image
sudo docker run --name cybersyn-postgres -p 5432:5432 -d postgres:9.4

# Run the julia docker image
sudo docker run -i
     --env=POSTGRES_PGPASS=password \
     --env=POSTGRES_PGUSER=username \
     --env=POSTGRES_DBNAME=cybersyn \
     --link cybersyn-postgres:postgres \
     -v /home/stucchio/src/cybersyn/:/var/lib/cybersyn/ \
     -t stucchio/juliaweb:0.3.2 /bin/bash
```

The `--link` option is used to connect the two docker images. This option will pass in two additional environment variables: `POSTGRES_PORT_5432_TCP_ADDR` and `POSTGRES_PORT_5432_TCP_PORT`. In production one should add extra `--env` arguments to provide these variables.

The second docker command just gets me a console inside a docker image that is ready for use. Also, the line `-v /home/stucchio/src/cybersyn/:/var/lib/cybersyn/` maps my native folder containing Julia code to a docker folder.

Here is some example code I can run from within the Julia docker container. You'll need to create the `users` table first:

```SQL
CREATE TABLE users (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    CONSTRAINT client_uuid_is_unique UNIQUE(id),
    CONSTRAINT client_name_is_unique UNIQUE(name)
);
```

Then you can write julia code against this:

```julia
module Storage

DB_HOST = ENV["POSTGRES_PORT_5432_TCP_ADDR"]
DB_PORT = ENV["POSTGRES_PORT_5432_TCP_PORT"]
DB_NAME = ENV["POSTGRES_DBNAME"]
DB_USER = ENV["POSTGRES_PGUSER"]
DB_PASS = ENV["POSTGRES_PGPASS"]

conn = connect(Postgres, DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT)

immutable User
    id::Int64
    name::ASCIIString
end

UserRef = Union(Int64,String)

user_ref(u::User) = u.id::UserRef

function save_user(name::ASCIIString)
    stmt = prepare(conn, "INSERT INTO users (name) VALUES (\$1);")
    try
        return execute(stmt, {name})
    finally
        finish(stmt)
    end
end

function get_user(ref::UserRef)
    stmt::DBI.StatementHandle
    if (typeof(ref)==ASCIIString)
        stmt = prepare(conn, "SELECT id, name FROM users WHERE name=\$1;")
    else
        stmt = prepare(conn, "SELECT id, name FROM users WHERE id=\$1;")
    end

    try
        result = execute(stmt, {ref})
        for row in result
            return User(row[1], row[2])
        end
    finally
        finish(stmt)
    end
end

end
```

Now you can run Julia from within it's docker image, call `save_user("zombie feynman")` from the command line and then verify that it's saved to the database.

# The webapp

Creating a very basic webapp is fairly straightforward given Julia's `Morsel.jl`:

```julia
using Storage
using Morsel
using PostgreSQL
using JSON

app = Morsel.app()

route(app, POST, "/api/users/<user>") do req, res
    username = convert(ASCIIString, req.state[:route_params]["user"])
    save_user(username)
    json(username)
end

route(app, GET, "/api/users/<user>") do req, res
    username = convert(ASCIIString, req.state[:route_params]["user"])
    user = get_user(username)
    json({ "username" => user.name, "id" => user.id })
end

start(app, 8000)
```

Unfortunately, doing more complicated things than simply returning JSON requires quite a bit of reading `Morsel.jl` code. From the docs alone, it's far from clear to me how I would do things like return a 404 error, change a `content-type` header, or anything of that sort. At some point in the future I may write a more detailed tutorial explaining how to do these things.

The webapp can then be run via:

```shell
docker run -i --env=POSTGRES_PGPASS=PASSWORD --env=POSTGRES_PGUSER=cybersyn --env=POSTGRES_DBNAME=adex \
    --link adex-postgres:postgres \
    --name julia_shell \
    -v /home/stucchio/src/cybersyn/:/var/lib/cybersyn/ \
    -p 8000:8000 \
    -t stucchio/juliaweb:0.3.2 "cd /var/lib/cybersyn && julia Web.jl"

```
In production, of course, port 8000 should not be exposed. Rather, the Julia webserver should be hidden behind a [revere proxy](http://jasonwilder.com/blog/2014/03/25/automated-nginx-reverse-proxy-for-docker/) - there is plenty of documentation on building a docker image with an nginx reverse proxy, so I'll just [link to it](http://jasonwilder.com/blog/2014/03/25/automated-nginx-reverse-proxy-for-docker/). Here is [my configuration](https://gist.github.com/stucchio/54331ebdee08bcadd051).

# Conclusion

Much as I love Julia for scientific computing, it isn't particularly easy at this time to deploy a microservice in Julia. The Julia ecosystem simply isn't ready at the moment. Nevertheless, if you want to do something very simple, Julia does provide the bare minimum tools needed to make it work. The procedure I describe here is one way to make things work. But more work will be needed before Julia is ready for deployment.
