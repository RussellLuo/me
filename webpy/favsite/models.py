#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""db.favsite: a collection for favsite app

   `postid`: as an interface parameter, should be a string (for consistency, an integer should be avoided although it's ok)
             as a return value, is always a string.
             as a collection field, is internally stored as an integer.
"""

import os
import logging
import web

from ..settings import IMG_PATH, DB
from utils.screenshot.screenshot_grabzit import getImgFromUrl

FAVSITE_IMG_PATH = IMG_PATH + '/favsite/'

# the favsite collection
favsite = DB.favsite

##### Interfaces #####

def insert(sitename, siteurl):
    imagename = _get_imagename(sitename)

    if favsite.sites.find_one({'name': sitename}):
        return 'repeated'
    elif getImgFromUrl(siteurl, imagename):
        favsite.sites.insert(dict(name=sitename, url=siteurl))
        return 'ok'
    else:
        return 'failed'

def remove(sitename):
    # remove image on disk
    imagename = _get_imagename(sitename)
    os.remove(imagename)

    # remove document in mongodb
    favsite.sites.remove({'name': sitename})

    return 'ok'

def clear():
    # remove all images on disk, borrowed from Blueicefield,
    # see http://stackoverflow.com/questions/185936/delete-folder-contents-in-python
    import glob
    images = glob.glob(FAVSITE_IMG_PATH + '/*')
    for f in images:
        os.remove(f)

    # remove all documents in mongodb
    favsite.sites.remove()

def get_all():
    cursor = favsite.sites.find().sort([('sitename', 1)])
    allsites = [site for site in cursor]
    return allsites
    
def _get_imagename(sitename):
    return FAVSITE_IMG_PATH + sitename + '.jpg'

# test
if __name__ == '__main__':
    import doctest
    doctest.testmod()
