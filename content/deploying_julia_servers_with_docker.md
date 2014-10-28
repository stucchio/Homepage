title: Deploying Julia Servers with Docker
date: 2014-11-01 09:00
author: Chris Stucchio
tags: julia, docker

Julia is a very nice little language. It's got a fast compiler, great numerical libraries, and integrates very easily with C. I'm hoping that as the world moves forward, Julia can eventually replace Python.

One thing Julia is *not* yet good for is web applications or other servers. In principle there is nothing that should prevent it from being used for this purpose, but the infrastructure, knowledge and libraries aren't there.

Since I'm deploying a Julia server, and since I found very little information on the web as to how this is done, I've decided to write up my experiences. Consider this blog post a set of notes explaining how I made it work - nothing more.

# Julia Packages

The first issue with building a deployable app is that Julia simply lacks a virtualenv. In fact, most of Julia's [package management system](http://julia.readthedocs.org/en/latest/manual/packages/) seems designed around building libraries that you install on your desktop and use for interactive sessions. There are two main methods for installing libraries - in the console, via `Pkg.add("mylib")`, or by adding entries to the *global* `REQUIRE` file.

Unlike Python, there is no equivalent of creating an application-specific `requirements.txt` file and then running `pip install -r requirements.txt`. One can, however, create *library* specific `REQUIRE` files which specify their dependencies.

The second issue with Julia packaging is that a lot of what you need to build a Julia program are C libraries - unfortunately, Julia's package management system does not handle this at all. Fortunately, such libraries can usually be installed in a fairly straightforward way with the operating system's package manager.

# Docker images

The first thing we'll do is create a base Julia docker image:

<script src="https://gist.github.com/stucchio/723108d4647fc83b151e.js"></script>

We then build the image with `$ sudo docker build -t stucchio/juliabase:0.3.2 .`.

We create a second docker image for the web stack:

<script src="https://gist.github.com/stucchio/4c5824d4716aad89c396.js"></script>

The file `REQUIRE` should be located in the same folder as this Dockerfile, and should list the required julia libraries.
