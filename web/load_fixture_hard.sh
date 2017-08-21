#!/usr/bin/env bash

# don't forget to delete db docker image first

cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
#echo "Flush database..."
#./manage.py sqlflush

echo "Delete temp files"
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

echo "Recreate migration folder"
rm -R api/migrations/*
touch api/migrations/__init__.py

python manage.py makemigrations && python manage.py migrate
python manage.py migrate --fake-initial
python manage.py migrate --run-syncdb

echo "Load fixture..."
manage.py loaddata fixture.json

migrate.sh
#./manage.py migrate --fake --run-syncdb