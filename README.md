me
==

The source code of my personal website.

Dependencies
------------

1. Python 2.6+
2. [web.py][]
3. MongoDB 2.4+
4. pymongo 2.6+
5. [markdown][]
6. [GrabzIt][]

Configuration
-------------

1) MetaWeblog settings

    $ vi webpy/blog/utils/config.py
    ...
    # now specially for www.cnblogs.com
    config = {
        'url':    'your_metaweblog_service_url',
        'appKey': '',
        'user':   'your_username',
        'passwd': 'your_password'
        }

2) GrabzIt settings

    $ vi webpy/favsite/utils/screenshot/screenshot_grabzit.py
    ...
    # my account at grabz.it
    config = {
        'applicationKey': 'your_key',
        'applicationSecret': 'your_secret'
        }

Initialize
----------

    $ ./init.sh

Run
---

    $ ./run.sh


[web.py]: https://github.com/webpy/webpy
[markdown]: https://github.com/waylan/Python-Markdown
[GrabzIt]: http://grabz.it/api/python/
