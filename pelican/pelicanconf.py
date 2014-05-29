#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime

AUTHOR = u'Chris Stucchio'
SITENAME = u'Chris Stucchio'
SITEURL = ''
PAGE_URL = '{slug}.html'
PAGE_PERMALINK_STRUCTURE = '/'
PAGE_SAVE_AS = '{slug}.html'

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'en'
STATIC_PATHS=['blog_media', 'work', 'pubs', 'media']

# Feed generation is usually not desired when developing
#FEED_ATOM = '/blog/atom.xml'
#FEED_ALL_ATOM = '/blog/atom.xml'
#FEED_ALL_ATOM = None
#FEEDS = [("All posts", "/blog/atom.xml")]
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

FILENAME_METADATA = '(?P<slug>.*)'
ARTICLE_PERMALINK_STRUCTURE = '/blog/%Y'
ARTICLE_URL = '{slug}.html'

DEFAULT_CATEGORY = ('Articles')
ARTICLE_EXCLUDES = ('pages',)

THEME = './theme/'
HIDE_SIDEBAR = True

DIRECT_TEMPLATES = ('index', 'tags', 'categories', 'archives', 'sitemap', 'atom')
SITEMAP_SAVE_AS = 'sitemap.xml'
ATOM_SAVE_AS = 'blog/atom.xml'

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

TODAY = datetime.now()
