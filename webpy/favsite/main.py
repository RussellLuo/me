#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import views

urls = (
  '/?', views.Index,
)

app = web.application(urls, globals())

# test
if __name__ == '__main__':
	app.run()
