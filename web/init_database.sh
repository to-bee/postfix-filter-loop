#!/usr/bin/env bash

#delete db.sqlite3
#delete all migrations

cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
pwd
rm db.sqlite3
rm -R monitoring/migrations/*
touch monitoring/migrations/__init__.py

python manage.py makemigrations && python manage.py migrate
python manage.py migrate --fake-initial
python manage.py migrate --run-syncdb
python manage.py createsuperuser