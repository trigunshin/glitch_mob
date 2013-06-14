#!/bin/bash

apt-get update
apt-get upgrade -y
apt-get update
apt-get install -y screen curl python-pip python-dev
# git-core python-virtualenv unzip python-setuptools libxml2-dev libxslt-dev

pip install -U pip fabric simplejson celery celery-with-redis requests
#beautifulsoup4

cd "/vagrant/"

cp "/vagrant/conf/celeryd.config" "/etc/default/celeryd"
cp "/vagrant/init.d/celeryd" "/etc/init.d"
chmod +x "/etc/init.d/celeryd"

CELERY_LOG_DIR="/var/log/celery"
CELERY_LOG="$CELERY_LOG_DIR/celery.log"

mkdir -p "$CELERY_LOG_DIR"
touch "$CELERY_LOG"
chown ubuntu:ubuntu "$CELERY_LOG"
chown ubuntu:ubuntu "$CELERY_LOG_DIR"

CELERY_PID_DIR="/var/run/celery"
#CELERY_PID_FILE="$CELERY_PID_DIR/celery.pid"
mkdir -p "$CELERY_PID_DIR"
#touch "$CELERY_PID_FILE"
chown ubuntu:ubuntu "$CELERY_PID_DIR"

/etc/init.d/celeryd start