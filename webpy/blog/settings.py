#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Settings for blog"""

import os
import sys

CURDIR = os.path.abspath(os.path.dirname(__file__))
PARDIR = CURDIR + '/..'

# character number for each article summray
SUMMARY_COUNT = 200

# posts per page
POSTS_PER_PAGE = 5 # 每页显示5篇文章

# cookie
COOKIE_EXPIRES_PAGEVIEW = 24*60*60 # 单位s，总共1天
COOKIE_EXPIRES_STAR = 365*24*60*60 # 单位s，总共1年

# cache
CACHE_SIZE = 50 # 最多缓存50篇文章
RESIZE_INTERVAL = 1*60*60 # 单位s，总共1小时
