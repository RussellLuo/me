#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import web

import models
from settings import CURDIR

render = web.template.render(CURDIR + '/templates/', base='layout', globals=dict(base_url='/', bg='#e5e5e5; url(/static/img/home_bg2.jpg)'))

class Index:
    def GET(self):
        return render.index(models.admin())

class About:
    def GET(self):
        return render.about(models.admin())

def notfound():
    return web.notfound(render.notfound(models.admin()))

def internalerror():
    return web.internalerror(render.internalerror(models.admin()))

# test
if __name__ == '__main__':
	pass
