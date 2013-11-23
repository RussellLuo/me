#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""usage: ./db_ctrl.py [cmd]

   cmd:
       init -- initialize favsite collection
       clr  -- clear favsite collection

"""

import models

sites = (
    {'name': u'百度', 'url': 'http://www.baidu.com'},
    {'name': u'Bootstrap', 'url': 'http://getbootstrap.com/'},
    {'name': u'博客园', 'url': 'http://www.cnblogs.com/russellluo/'},
    {'name': u'CSDN', 'url': 'http://www.csdn.net/'},
    {'name': u'Digg', 'url': 'http://digg.com/'},
    {'name': u'有道词典', 'url': 'http://dict.youdao.com/'},
    {'name': u'豆瓣', 'url': 'http://www.douban.com/people/RussellLuo/'},
    {'name': u'GitHub', 'url': 'https://github.com/'},
    {'name': u'GoDaddy', 'url': 'http://www.godaddy.com/'},
    {'name': u'Google', 'url': 'https://www.google.com.hk/'},
    {'name': u'Google Groups', 'url': 'https://groups.google.com/forum/?hl=en#!overview'},
    {'name': u'爱奇异', 'url': 'http://www.iqiyi.com/'},
    {'name': u'Instapaper', 'url': 'http://www.instapaper.com/u'},
    {'name': u'IVORY', 'url': 'http://weice.in/ivory/'},
    {'name': u'OpenShift', 'url': 'https://www.openshift.com/'},
    {'name': u'Python', 'url': 'http://www.python.org/'},
    {'name': u'reddit', 'url': 'http://www.reddit.com/'},
    {'name': u'Slashdot', 'url': 'http://slashdot.org/'},
    {'name': u'Stack Overflow', 'url': 'http://stackoverflow.com/'},
    {'name': u'web.py', 'url': 'http://webpy.org/'},
    {'name': u'新浪微博', 'url': 'http://weibo.com/luopengblog'}
)

"""This following functions are for management convenience,
   they should be called manually by manager at system-level.
"""

def init():
    """initialize favsite collection using images saved locally
    """
    import glob
    import shutil

    images = glob.glob(models.FAVSITE_IMG_PATH + '/../backup/jpg/*')
    for f in images:
        shutil.copy(f, models.FAVSITE_IMG_PATH)

    for s in sites:
        models.favsite.sites.insert(s)

def clr():
    """clear favsite collection
    """
    models.clear()

# test
if __name__ == '__main__':
    import sys
    if not (len(sys.argv) == 2 and sys.argv[1] in globals()):
        sys.stderr.write(__doc__)
    else:
        globals()[sys.argv[1]]()
