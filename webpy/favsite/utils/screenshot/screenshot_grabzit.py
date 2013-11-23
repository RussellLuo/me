#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Get a webpage screenshot from URL by GrabzIt.

See: http://grabz.it/api/python/
"""

import urllib2
import logging
from GrabzIt import GrabzItClient

# my account at grabz.it
config = {
    'applicationKey': 'your_key',
    'applicationSecret': 'your_secret'
}

# create a GrabzItClient instance
grabzIt = GrabzItClient.GrabzItClient(**config)

def getImgFromUrl(url, savePath, width=200, height=200, format='jpg'):
    """Get a screenshot of the webpage at `url`, then save the image into `savePath`.

        >>> import os
        >>> savePath = 'baidu.jpg'
        >>> os.path.isfile(savePath)
        False
        >>> getImgFromUrl('http://www.baidu.com', savePath)
        True
        >>> os.path.isfile(savePath)
        True
        >>> os.remove(savePath)
    """

    # first, check if `url` is reachable
    try:
        urllib2.urlopen(url, timeout=15)
    except urllib2.URLError, e:
        logging.warning(str(e))
        return False

    # then, get a screenshot and save it
    try:
        grabzIt.SetImageOptions(url, width=width, height=height, format=format)
        grabzIt.SaveTo(savePath) # synchonous method, may be blocked for a while
    except Exception, e:
        logging.error(str(e))
        return False

    return True

# test
if __name__ == '__main__':
    import doctest
    doctest.testmod()
