#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
import pickle
import web

from settings import DB, COOKIE_EXPIRES_ADMIN

# the home collection
home = DB.home

##### Interfaces #####

def login(pwd):
    """Log in if `pwd` is correct
    """
    if not _authenticate(pwd):
        return False

    # 设置cookie
    pwdhash = hashlib.md5(pwd).hexdigest()
    web.setcookie('admin', pwdhash, settings.COOKIE_EXPIRES_ADMIN)

    return True

def admin():
    """Check if this is the administrator
    """
    pwd = web.cookies().get('admin')
    if not _authenticate(pwd):
        return False

    # 刷新cookie
    pwdhash = hashlib.md5(pwd).hexdigest()
    web.setcookie('admin', pwdhash, settings.COOKIE_EXPIRES_ADMIN)

    return True

def update(new_pwd):
    """Modify the password using `new_pwd`
    """
    home.admin.update({'admin': 'russellluo'}, {"$set" : {"pwd" : new_pwd}})

##### Internal help function #####

def _authenticate(pwd):
    """Do authentication to check if `pwd` is correct
    """
    if not pwd:
        return False

    correct_pwd = home.admin.find_one({'admin': 'russellluo'}).get('pwd')
    return pwd == correct_pwd

def _init(ori_pwd):
    """Initialize the admin account using `ori_pwd` as the original password

       Note: this function should be called by manager at system level
    """
    home.admin.insert({'admin': 'russellluo', 'pwd': ori_pwd})

# test
if __name__ == '__main__':
	pass
