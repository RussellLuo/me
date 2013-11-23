#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Publish a post

usage as script:
    ./publish.py <title> <markdown_filename>
    ./publish.py <html_filename>
"""

import sys
import codecs
import markdown
import post

def publish_markdown(title, filename):
    """Publish a markdown post"""

    markdown_file = codecs.open(filename, 'r', encoding='utf-8')
    text = markdown_file.read()

    description = markdown.markdown(text, extensions=['extra', 'toc'])
    description = '<div id="markdown">\n\n%s\n\n</div>' % description

    post.new(title, description)

def publish_html(filename):
    """Publish a html post"""

    html_file = codecs.open(filename, 'r', encoding='utf-8')
    content = html_file.read()

    title, description = post.parse_html(content)
    post.new(title, description)

# test
if __name__ == '__main__':
    arglen = len(sys.argv)
    try:
        if arglen == 3:
            publish_markdown(sys.argv[1], sys.argv[2])
            print 'succeeded'
        elif arglen == 2:
            publish_html(sys.argv[1])
            print 'succeeded'
        else:
            sys.stderr.write(__doc__)
    except Exception, e:
        print 'failed'
