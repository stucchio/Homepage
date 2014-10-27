#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://www.chrisstucchio.com'
#SITEURL = 'http://cs-blog-preview.s3-website-us-east-1.amazonaws.com'

RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "chrisstucchiosblog"
GOOGLE_ANALYTICS = "UA-30538320-1"
BAYESIAN_WITCH_SITE_ID = 'cdfdf2e8-8937-4fa8-9a5b-7595f8b3487f'
BAYESIAN_WITCH_SITE_DOMAIN = 'chrisstucchio.com'

DEBUG = False
