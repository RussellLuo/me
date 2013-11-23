#!/bin/bash

regen ()
{
    workdir=$1

    cd $workdir
    rm -f static
    ln -s ../static static

    cd $workdir/templates
    rm -f layout.html
    ln -s ../../templates/layout.html layout.html
}

topdir=$(pwd)

## 1. Regenerate symbol links for the current system (32 or 64)

# for main app
cd $topdir/webpy
rm -f static
ln -s ../static static

# for subapps
basedir=$(pwd)
regen $basedir/blog
regen $basedir/favsite
regen $basedir/follow
regen $basedir/bookmark
regen $basedir/about

## 2. Initialize database for subapp "blog"
cd $topdir
python -m webpy.blog.db_ctrl clr
python -m webpy.blog.db_ctrl init
python -m webpy.blog.db_ctrl trim

## 3. Initialize database for subapp "favsite"
python -m webpy.favsite.db_ctrl clr
python -m webpy.favsite.db_ctrl init
