#!/usr/bin/env python
# -*- coding: utf-8 -*-
import markdown
import sys

if len(sys.argv) != 3:
    print 'usage: python markdown2html.py [markdown_filename] [html_filename]'

try:
    markdown.markdownFromFile(input=sys.argv[1], output=sys.argv[2], extensions=['extra', 'toc'])
    print 'succeeded'
except Exception, e:
    print 'failed'
