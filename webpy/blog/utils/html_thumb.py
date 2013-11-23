#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Get a thumb (i.e. the 1st <img>) from the HTML-format text"""

import re

def get_thumb(text, default=''):
    """Get the src-URL of the first <img> tag in `text`, return `default` if no <img> exists

        >>> get_thumb('<img src="http://www.python.org/images/python-logo.gif" python-logo />')
        'http://www.python.org/images/python-logo.gif'
    """
    res = re.search(r'<img\s+src\s*=\s*"(.*?)"(.*?)/>', text, re.S | re.I)
    return res.group(1) if res else default

# test
if __name__ == '__main__':
    import doctest
    doctest.testmod()
