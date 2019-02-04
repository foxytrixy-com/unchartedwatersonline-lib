#!/bin/bash 

set -e
set -u

FILE_DIR=$(dirname `readlink -f ${0}`)
# FILE_DIR=`pwd`/../scripts
SCRIPTS_DIR=$FILE_DIR
BASE_DIR=$(dirname $SCRIPTS_DIR)
WEB_DIR=$BASE_DIR/web
LOG_DIR=$WEB_DIR/log

git checkout develop
git pull origin develop
$WEB_DIR/manage.py migrate

git checkout master
git merge --no-ff develop

# $SCRIPTS_DIR/django2mod_wsgi.bash
# sudo service apache2 restart

