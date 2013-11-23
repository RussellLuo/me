#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import web
import json

import models
from utils.html_summary import get_summary
from utils.html_thumb import get_thumb
from settings import *

from ..models import admin

render = web.template.render(CURDIR + '/templates/', base='layout', globals=dict(base_url='/blog', bg='url(/static/img/bg.jpg)'))

class Index:
    def GET(self):
        try:
            i = web.input(page='1', do_sync=False)

            # get parameters from URL
            page_id = int(i.page)
            do_sync = bool(i.do_sync)

            # get posts (may do synchronizing)
            posts = models.recent((page_id-1) * POSTS_PER_PAGE, POSTS_PER_PAGE, do_sync)
            for p in posts:
                p['summary'] = get_summary(unicode(p['description']), SUMMARY_COUNT, suffix=u'...').encode('utf-8')
                p['thumb'] = get_thumb(unicode(p['description']), '')

            # get page count
            div, mod = divmod(models.count(), POSTS_PER_PAGE)
            page_count = div + (1 if mod else 0)

            return render.index(posts, page_id, page_count, admin())
        except Exception:
            raise web.notfound()

class View:
    def GET(self, postid):
        try:
            # increase pageview if necessary
            if is_new_pageview(postid):
                models.inc_pageviews(postid)

            p = models.get(postid)
            if p:
                return render.view(p, admin())
            else:
                raise web.notfound()
        except Exception:
            raise web.notfound()

    def POST(self, postid):
        try:
            i = web.input(do_recommend=False)
            do_recommend = bool(i.do_recommend)

            web.header('Content-Type', 'application/json')

            if do_recommend and is_new_star(postid):
                models.inc_starred(postid)
                new_starred = models.get(postid).get('starred', 0)
                return json.dumps({'status': 'ok', 'starred': new_starred})
            else:
                return json.dumps({'status': 'repeated'})
        except Exception:
            return json.dumps({'status': 'failed'})

def is_new_pageview(postid):
    """Judge if it's a valid new PAGEVIEW by cookies based on postid"""

    flag = 'pageview_' + postid

    if web.cookies().get(flag):
        return False
    else:
        web.setcookie(flag, '1', COOKIE_EXPIRES_PAGEVIEW)
        return True

def is_new_star(postid):
    """Judge if it's a valid new STAR by cookies based on postid"""

    flag = 'star_' + postid

    if web.cookies().get(flag):
        return False
    else:
        web.setcookie(flag, '1', COOKIE_EXPIRES_STAR)
        return True

# test
if __name__ == '__main__':
    pass
