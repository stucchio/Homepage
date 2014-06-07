title: Mosh - ssh for a bad connection
date: 2014-05-17 09:00
author: Chris Stucchio
tags: mosh, ssh, india
nolinkback: true





I'm currently located in India. Most of my servers are in the US. Due to my location, I have to deal with crappy wifi connections (in the past hour I switched from NETGEAR1 to NETGEAR2), high latency, disconnections and the like. Often I'm stuck tethered to my phone, which occasionally results in my IP address changing.

Enter [Mosh](http://mosh.mit.edu/). It's a mobile SSH tool designed for crappy connections. Usage is simple.

On the client and server, simply install mosh:

    $ apt-get install mosh

From the client:

    $ mosh username@direct.myhostname.com

For the most part, you can just use it like SSH.

Just throwing this out there in the hope that some of my readers need this but don't know about it. Mosh is a great tool and I don't know why more people don't know about it.


