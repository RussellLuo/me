#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import web
from utils import post

curdir = os.path.abspath(os.path.dirname(__file__))
render = web.template.render(curdir + '/templates/', base='layout')

class ReIndex:
    def GET(self):
        raise web.seeother('/')

class Index:
    def GET(self):
        ps = post.recent(1)
        return render.index(ps)

class View:
    def GET(self, postid):
        p = post.get(postid)
        return render.index([p])

# test
if __name__ == '__main__':
	pass
