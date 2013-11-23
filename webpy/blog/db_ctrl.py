#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""usage: ./db_ctrl.py [cmd]

   cmd:
       init -- initialize blog collection
       trim -- trim blog collection
       clr  -- clear blog collection

"""

import models

"""This following functions are for management convenience,
   they should be called manually by manager at system-level.
"""

def init():
    """initialize blog collection
    """
    # synchronize articles from http://www.cnblogs.com/russellluo/archive/2013/06/15/3137270.html
    models.insert('3137270') # insert a post into blog.posts

def trim():
    """remove unnecessary data from blog collection
    """
    # these posts are unpublished, so remove them from blog.posts
    for postid in ('3139542', '3177535', '3179264', '3180481', '3186614', '3197396', '3200131'):
        models.remove(postid)

def clr():
    """clear blog collection
    """
    models.clear() # remove all posts
    models.blog.cache.remove() # remove all cached posts, too

# test
if __name__ == '__main__':
    import sys
    if not (len(sys.argv) == 2 and sys.argv[1] in globals()):
        sys.stderr.write(__doc__)
    else:
        globals()[sys.argv[1]]()
