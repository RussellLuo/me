#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import web

import models
from ..models import admin

curdir = os.path.abspath(os.path.dirname(__file__))
render = web.template.render(curdir + '/templates/', base='layout', globals=dict(base_url='/favsite', bg='#e5e5e5'))

class Index:
    def GET(self):
        sites = models.get_all()
        return render.index(sites, True) #admin())

    def POST(self):
        i = web.input(action='', sitename='', siteurl='')

        web.header('Content-Type', 'application/json')

        if i.action == 'add':
            return json.dumps(models.insert(i.sitename, i.siteurl))
        elif i.action == 'remove':
            return json.dumps(models.remove(i.sitename))
        else:
            return json.dumps('none')

# test
if __name__ == '__main__':
    pass
