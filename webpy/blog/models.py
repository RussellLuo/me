#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""db.blog: a collection for blog app

   `postid`: as an interface parameter, should be a string (for consistency, an integer should be avoided although it's ok)
             as a return value, is always a string.
             as a collection field, is internally stored as an integer.
"""

import os
import threading
import time
import pickle
import logging
import web

from utils import post
from settings import CURDIR, CACHE_SIZE, RESIZE_INTERVAL
from ..settings import DB

# the blog collection
blog = DB.blog

# defined so early here because it will be used in "module init"
def _resize_cache():
    """A thread specially for resizing the posts in cache collection
    """
    while True:
        try:
            cache_lock.acquire()
            try:
                cached_posts = blog.cache.find().sort([('savetime', 1)]) # from old to new
                count = cached_posts.count()

                # remove the oldest posts to keep size
                if count > CACHE_SIZE:
                    post_ids = [p['postid'] for p in cached_posts[0:count-CACHE_SIZE]]
                    for p_id in post_ids:
                        blog.cache.remove({'postid': p_id})
            except Exception:
                raise
            finally:
                cache_lock.release()

            # do the task periodically
            time.sleep(RESIZE_INTERVAL)

        except (KeyboardInterrupt, SystemExit):
            logging.info('program exits')
            break

# module init
try:
    _init_flag
except Exception:
    _init_flag = True

    # lock for cache collection
    cache_lock = threading.Lock()

    # start a thread for _resize_cache
    resize_thread = threading.Thread(target=_resize_cache, name='_resize_cache')
    resize_thread.daemon = True # see http://stackoverflow.com/questions/3788208/python-threading-ignores-keyboardinterrupt-exception
    resize_thread.start()

##### Interfaces #####

def insert(postid):
    blog.posts.insert(dict(postid=int(postid), pageviews=0, starred=0))

def remove(postid):
    blog.posts.remove({'postid': int(postid)})

def clear():
    blog.posts.remove()

def inc_pageviews(postid):
    blog.posts.update({'postid': int(postid)}, {'$inc': {'pageviews': 1}})

def inc_starred(postid):
    blog.posts.update({'postid': int(postid)}, {'$inc': {'starred': 1}})

def get(postid):
    cursor = blog.posts.find_one({'postid': int(postid)})
    if not cursor:
        return {}
    else:
        '''
        # get original post (cache via file)
        postpath = '%s/cache/%s.post' % (CURDIR, postid)
        if os.path.isfile(postpath): # get post from file if possible
            p = pickle.load(open(postpath, 'rb'))
        else:
            p = post.get(postid) # get remotely
            pickle.dump(p, open(postpath, 'wb'), pickle.HIGHEST_PROTOCOL) # save into file for next usage
        '''

        feedback = dict(pageviews=cursor['pageviews'], starred=cursor['starred'])

        # if cache collection is being accessed by other one (only can be _resize_cache so far)
        if not cache_lock.acquire(False):
            return _add_feedback(_get_remotely(postid), feedback)
        else:
            try:
                # get the post from cache if possible
                cached_post = blog.cache.find_one({'postid': int(postid)})
                if cached_post:
                    return _add_feedback(cached_post.get('post', {}), feedback)
                else:
                    p = _get_remotely(postid)
                    if not p:
                        return {}

                    # cache for next usage
                    blog.cache.insert({'postid': int(postid), 'savetime': time.time(), 'post': p})

                    return _add_feedback(p, feedback)
            finally:
                cache_lock.release()
    
def recent(offset=0, number=5, do_sync=False):
    '''Synchronize articles

       if `do_sync` is True, always do synchronizing 
       else, to enhance user experience, do synchronizing automatically per hour
    '''
    if do_sync or _time_out(1*60*60, do_sync):
        _sync_remotely()

    res = []
    for postid in _find_ids(offset, number):
        p = get(unicode(postid))
        if p:
            res.append(p)
    return res

def count():
    cursor = blog.posts.find()
    return cursor.count()

##### Internal help function #####

def _get_remotely(postid):
    """Get the post from remote"""

    # get the raw post remotely
    p = post.get(postid)
    if not p:
        return {}

    '''get the final post by modifying the raw one'''

    # 1. convert datetime type
    post.adjust(p)

    # 2. get ids for previous post and next post (relative to current post)
    # (1) get previous postid
    new_cursor = blog.posts.find({'postid': {'$lt': int(postid)}}).sort([('postid', -1)])
    try:
        p['postid_prev'] = new_cursor[0].get('postid', 0)
    except IndexError:
        p['postid_prev'] = 0
    # (2) get next postid
    new_cursor = blog.posts.find({'postid': {'$gt': int(postid)}}).sort([('postid', 1)])
    try:
        p['postid_next'] = new_cursor[0].get('postid', 0)
    except IndexError:
        p['postid_next'] = 0

    return p

def _add_feedback(p, feedback):
    """Add user feedback information such as `pageviews` and `starred` into `p`
    """
    if p and 'pageviews' in feedback and 'starred' in feedback:
        p.update(feedback)

    return p

def _find_ids(offset, number):
    # get `number` rencent posts starting from `offset`
    cursor = blog.posts.find({}, {'postid': 1, '_id': 0}).sort([('postid', -1)])

    '''Apply skip and limit with cursor

       see http://api.mongodb.org/python/current/api/pymongo/cursor.html#pymongo.cursor.Cursor.__getitem__
    '''
    start, end = offset, offset + number
    ps = cursor[start:end]

    # `postid` returned here are still integers
    return [c['postid'] for c in ps]

BASE_TIME = time.time()
def _time_out(seconds, reset=False):
    """Detect if the specified time is out

       if 'reset' is True, BASE_TIME is set to current time (i.e. now)
    """

    global BASE_TIME

    if reset:
        BASE_TIME = time.time()

    if int(time.time() - BASE_TIME) >= seconds:
        BASE_TIME = time.time()
        return True
    else:
        return False

def _sync_remotely():
    """Synchronize posts from remote blog-system (cnblogs)"""

    #print 'do synchronizing...'

    # get current max-postid in database
    ids = _find_ids(0, 1)
    cur_max_postid = ids[0] if ids else 0

    num_to_get = 5
    while True:
        try:
            latest_posts = post.recent(num_to_get)
            latest_ids = [int(p['postid']) for p in latest_posts]

            # we've gotten all the latest posts possible
            if min(latest_ids) <= cur_max_postid:
                for postid in latest_ids:
                    if postid > cur_max_postid:
                        insert(unicode(postid))
                break # task is done, get out

            # maybe some new posts are missed, we need to check more
            num_to_get += 5

        except ValueError:
            break

"""This following functions are for management convenience,
   they should be called manually by manager at system-level.
"""
def _init_posts():
    """initialize collection blog.posts"""
    # synchronize articles from http://www.cnblogs.com/russellluo/archive/2013/06/15/3137270.html
    insert('3137270')

def _trim_posts():
    """remove unnecessary posts from blog.posts"""
    # these posts are unpublished
    for postid in ('3139542', '3177535', '3179264', '3180481', '3186614', '3197396', '3200131'):
        remove(postid)

def _clr_posts():
    """clear collection blog.posts"""
    remove()


def __test():
    """Doc-Test specially for cursor object of pymongo,
       for more details, see http://api.mongodb.org/python/current/api/pymongo/cursor.html#pymongo.cursor.Cursor.

       Note: For find() method, the key difference between `cursor` and `cursor[skip:skip+limit]` is the latter is limited and skipped.
    
        >>> cursor = blog.posts.find_one({'postid': 3137270})
        >>> type(cursor), bool(cursor)
        (<type 'dict'>, True)
        >>> cursor = blog.posts.find({'postid': 3137270})
        >>> type(cursor), bool(cursor)
        (<class 'pymongo.cursor.Cursor'>, True)
        >>> type(cursor[0:2]), bool(cursor[0:2])
        (<class 'pymongo.cursor.Cursor'>, True)
        >>> type(cursor[0]), bool(cursor[0])
        (<type 'dict'>, True)
    """
    pass

# test
if __name__ == '__main__':
    import doctest
    doctest.testmod()
