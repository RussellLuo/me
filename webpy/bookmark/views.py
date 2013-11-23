#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import web

from ..models import admin

curdir = os.path.abspath(os.path.dirname(__file__))
render = web.template.render(curdir + '/templates/', base='layout', globals=dict(base_url='/bookmark', bg='#e5e5e5'))

class Index:
    def GET(self):
        return render.index(admin())

# test
if __name__ == '__main__':
	pass
