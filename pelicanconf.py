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
EXTRA_PATH_METADATA = { 'media/favicon.ico' : {'path' : 'favicon.ico' } }

# Feed generation is usually not desired when developing
#FEED_ATOM = None
FEED_ALL_ATOM = None
#FEED_ALL_ATOM = None
#FEEDS = [("All posts", "/blog/atom.xml")]
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

FILENAME_METADATA = '(?P<slug>.*)'
#ARTICLE_PERMALINK_STRUCTURE = '/blog/%Y'
ARTICLE_URL = 'blog/{date:%Y}/{slug}.html'
ARTICLE_LANG_URL = 'blog/{date:%Y}/{slug}-{lang}.html'
PAGE_URL = 'blog/{date:%Y}/{slug}.html'
PAGE_LANG_URL = 'blog/{date:%Y}/pages/{slug}-{lang}.html'
DRAFT_URL = 'blog/{date:%Y}/drafts/{slug}.html'
DRAFT_LANG_URL = 'blog/{date:%Y}/drafts/{slug}-{lang}.html'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{slug}.html'
ARTICLE_LANG_SAVE_AS = 'blog/{date:%Y}/{slug}-{lang}.html'
DRAFT_SAVE_AS = 'blog/{date:%Y}/drafts/{slug}.html'
DRAFT_LANG_SAVE_AS = 'blog/{date:%Y}/drafts/{slug}-{lang}.html'
PAGE_SAVE_AS = '{slug}.html'
PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}.html'


DEFAULT_CATEGORY = ('Articles')
ARTICLE_EXCLUDES = ('pages',)

THEME = './theme/'
HIDE_SIDEBAR = True

DIRECT_TEMPLATES = ('index', 'blog_index', 'tags', 'categories', 'archives', 'sitemap', 'atom')
SITEMAP_SAVE_AS = 'sitemap.xml'
ATOM_SAVE_AS = 'blog/atom.xml'
BLOG_INDEX_SAVE_AS = "blog/index.html"
PAGINATED_DIRECT_TEMPLATES = ['blog_index']

FRONT_PAGE_CATEGORIES = [ 'high frequency trading', 'conversion rate optimization', 'scala', "bandit algorithms"]

DISPLAY_CATEGORIES_ON_MENU = False

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10
DEBUG = True

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

TODAY = datetime.now()

PLUGIN_PATHS = ['plugins/m.css/pelican-plugins']
PLUGINS = ['m.htmlsanity', 'm.math',  'm.abbr']
