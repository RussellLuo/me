#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Get a 'first-N characters' summary from the HTML-format text"""

from HTMLParser import HTMLParser

class SummaryHTMLParser(HTMLParser):
    """Parse HTML text to get a summary

        >>> text = u'<p>Hi guys:</p><p>This is a example using SummaryHTMLParser.</p>'
        >>> parser = SummaryHTMLParser(10)
        >>> parser.feed(text)
        >>> parser.get_summary('p')
        u'<p>Higuys:Thi</p>'
    """
    def __init__(self, count):
        HTMLParser.__init__(self)
        self.count = count
        self.summary = u''

    def handle_data(self, data):
        more = self.count - len(self.summary)
        if more > 0:
            '''Remove whitespace in `data`
               see http://stackoverflow.com/questions/1898656/remove-whitespace-in-python-using-string-whitespace
               thank bobince for this concise method!
            '''
            data_without_whitespace = u''.join(unicode(data).split())

            self.summary += data_without_whitespace[0:more]

    def get_summary(self, tag, suffix=u''):
        return u'<{0}>{1}{2}</{0}>'.format(unicode(tag), self.summary, suffix)

def get_summary(text, count, tag='p', suffix=u''):
    """A SummaryHTMLParser wrapper function for convenience

        >>> text = u'<p>Hi guys:</p><p>This is a example using SummaryHTMLParser.</p>'
        >>> get_summary(text, 10, suffix=u'...')
        u'<p>Higuys:Thi...</p>'
    """
    parser = SummaryHTMLParser(count)
    parser.feed(text)
    return parser.get_summary(tag, suffix)

# test
if __name__ == '__main__':
    import doctest
    doctest.testmod()
