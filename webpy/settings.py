#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Settings for this site"""

import os
import logging
import datetime

CURDIR = os.path.abspath(os.path.dirname(__file__))
today = datetime.datetime.today()

IMG_PATH = CURDIR + '/static/img'

# for logging
LOGPATH = CURDIR + '/logs/'
LOGFILE = LOGPATH + today.strftime('%Y-%m-%d') + '.log'
LOGLEVEL = logging.WARNING

# admin authentication cookie
COOKIE_EXPIRES_ADMIN = 1*60*60 # 单位s，总共1小时

# for MongoDB
'''
"""OpenShift only support MongoDB 2.2 now, so I have to use `Connection`

   Note: For MongoDB 2.2, the corresponding version of pymongo is 2.3 (see http://api.mongodb.org/python/2.3/changelog.html),
   documentation for pymongo 2.3 is at http://api.mongodb.org/python/2.3/api/index.html
"""
from pymongo import Connection
HOST = os.environ['OPENSHIFT_MONGODB_DB_HOST']
PORT = os.environ['OPENSHIFT_MONGODB_DB_PORT']
# for URI format, see http://docs.mongodb.org/manual/reference/connection-string/ and
# http://stackoverflow.com/questions/15562279/mongooperationfailure-need-to-login-when-using-from-uri
URI = 'mongodb://admin:nV8PfeJtRwSv@{0}:{1}/me'.format(HOST, PORT)
DB = Connection(URI).me

'''
## I have installed MongoDB 2.4 and pymongo 2.6 in my local machine, so `MongoClient` is ok
from pymongo import MongoClient
DB = MongoClient().me
