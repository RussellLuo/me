#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

import views

urls = (
  '/?', views.Index,
  '/view/(\d+)', views.View,
)

app = web.application(urls, globals())

# test
if __name__ == '__main__':
	app.run()
