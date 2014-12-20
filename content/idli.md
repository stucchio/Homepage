title: Idli - a command line interface to your bugtracker
date: 2012-04-24 10:00
author: Chris Stucchio
tags: development, bug tracking, python





A while back, Hacker News was deluged with [assorted](http://news.ycombinator.com/item?id=1620168) [command](http://roundup-tracker.org/docs.html) [line](http://ditz.rubyforge.org/) [bug trackers](http://bugseverywhere.org/). It's pretty clear that many people want a command line interface to their bug tracking system. But most of us are forced to use an existing system and can't switch to such a new one. So I wrote [Idli](https://github.com/stucchio/Idli), which is a command line *interface* to existing bug trackers.





[Idli](https://github.com/stucchio/Idli) is capable of interfacing with multiple different backends - currently [github](http://github.com), [trac](http://trac.edgewall.org/) and [redmine](http://redmine.org). It offers a simplified interface which exposes some (though not all) the features of the underlying bug tracker.

Idli is used in a fairly simple way. For github:

    $ idli config github USERNAME PASSWORD

The config command configures *global* variables, which are stored in `$HOME/.idli_config`.

To use it on a project, you do it as follows:

    $ git clone git@github.com:stucchio/Idli.git
    $ cd idli
    $ idli config github idli stucchio

A file .idli is created which saves these parameters. This points your idli project to the github idli issue tracker.

You can list issues:

    $ idli list
    ID     date        title                                creator       owner       # comments
    2      2010/09/22  Need better documentation            stucchio                  0
    3      2010/09/22  Bitbucket backend                    stucchio                  0
    5      2010/09/22  Search for bugs                      stucchio                  1
    6      2010/09/28  Add bugzilla backend                 stucchio                  1
    7      2010/09/29  Add lightweight backend (no server)  stucchio                  0
    15     2010/10/03  Tagging support in trac              stucchio                  0
    21     2012/04/22  Redmine support                      stucchio                  0
    26     2012/04/22  Pivotal tracker backend              stucchio                  0

Issues can be viewed in more detail:

    $ idli show 5
    ID: 5
    Title: Search for bugs
    Creator: stucchio
    Create time: 2010-09-22 11:58:20
    Open: True
    Tags: search

    Search functionality would be useful.

    In principle, we could create a default implementation which does the search on the local computer
    (based on listing all bugs).

    Comments:

        Author: stucchio
        Date: 2010-10-05 06:45:21

        To clarify, this should be a full text search.

        It should be based on comments, title, description, etc.


If you wish to add an issue, you merely type `idli add` - your text editor will pop up and ask you to create the issue, in much the same way git asks you for commit messages. Alternately you can specify on the command line:

    $ idli add --title "The frobnicator is broken." --body "The frobnicator does not frobnicate."

 To resolve an issue, you type `idli resolve ID`, and the editor will behave in a similar manner. The editor is defined in the environment variable `$EDITOR`, just as with git.

Idli has backends for trac and redmine as well. Writing a new backend is fairly straightforward - it involves overriding `idli.Backend` and implementing the methods `add_issue`, `tag_issue`, etc. See the `Backend` class in [idli.py](https://github.com/stucchio/Idli/blob/master/idli/__init__.py) for a full list - any method which raises an `IdliNotImplementedException` should be overridden (if the backend supports that functionality).

If anyone wants to write a backend for their favorite bug tracker, I welcome contributions. I've mostly just written backends for the bug trackers I use, but I'd love a backend for your favorite one as well.

Code is available on [github](https://github.com/stucchio/Idli).
