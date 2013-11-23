#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

import blog
import favsite
import follow
import bookmark
import about
import views

import logging
from settings import LOGFILE, LOGLEVEL
logging.basicConfig(filename=LOGFILE, level=LOGLEVEL, format='%(asctime)s : %(levelname)s : %(message)s')

urls = (
  '/', views.Index,
  '/blog', blog.app,
  '/favsite', favsite.app,
  '/follow', follow.app,
  '/bookmark', bookmark.app,
  '/about', about.app,
)

# disable the debug mode
web.config.debug = False
app = web.application(urls, globals())

# custom notfound and internalerror
for a in (app, blog.app, favsite.app,
          follow.app, bookmark.app, about.app):
    a.notfound = views.notfound
    a.internalerror = views.internalerror

# export a wsgi-compatible application
application = app.wsgifunc()

# test
if __name__ == '__main__':
    app.run()
