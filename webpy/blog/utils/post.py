#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convenient interfaces for operating HTML-format post"""

import re
from datetime import datetime
from urlparse import urlparse
from metaweblog import MetaWeblog
from config import config

weblog = MetaWeblog(**config)

##### Interfaces #####

def new(title, description, mt_keywords='', publish=True, **kwargs):
    description = handle_img(description)
    return weblog.newPost(title, description, mt_keywords, publish, **kwargs)

def edit(postid, title, description, mt_keywords='', publish=True, **kwargs):
    description = handle_img(description)
    return weblog.editPost(postid, title, description, mt_keywords, publish, **kwargs)

def delete(postid):
    return weblog.deletePost(postid)

def get(postid):
    return weblog.getPost(postid)

def recent(count=5):
    return weblog.getRecentPosts(count)

def parse_html(content):
    """Parse HTML file to get title and description (i.e. body)

        >>> content = '''
        ... <html>
        ...     <head>
        ...         <title>Greetings</title>
        ...     </head>
        ...     <body>
        ...         <p>Hello World!</p>
        ...     </body>
        ... </html>
        ... '''
        >>> parse_html(content)
        ('Greetings', '<p>Hello World!</p>')
    """

    res = re.search(r'<title>(.*?)</title>', content, re.S | re.I)
    title = res.group(1) if res else 'untitled'

    res = re.search(r'<body>(.*?)</body>', content, re.S | re.I)
    description = res.group(1) if res else 'no description'

    return title.strip(), description.strip()

def adjust(p):
    if not p.get('dateCreated'):
        return

    # convert xmlrpclib.DateTime to datetime.datetime
    p['dateCreated'] = datetime.strptime(p['dateCreated'].value, "%Y%m%dT%H:%M:%S")
    # get a formatted time sting
    p['dateCreated'] = p['dateCreated'].strftime('%Y-%m-%d %H:%M')

##### Internal help function #####

def repl_src(m):
    """Replace image src: from filesystem-path to internet-url"""

    path = m.group(1)
    other = m.group(2)

    # path may be actually an url
    o = urlparse(path)
    if o.scheme in ('http', 'https'):
        newpath = path # nothing changed
    else:
        newpath = weblog.newMediaObject(path).get('url', path) # url of new-uploaded image

    return '<img src="%s"%s/>' % (newpath, other)

def handle_img(description):
    """Handle each image reference

        >>> handle_img('<img src="http://www.python.org/images/python-logo.gif" python-logo />')
        '<img src="http://www.python.org/images/python-logo.gif" python-logo />'
    """

    return re.sub(r'<img\s+src\s*=\s*"(.*?)"(.*?)/>', repl_src, description)

# test
if __name__ == '__main__':
    import doctest
    doctest.testmod()
