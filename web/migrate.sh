#!/bin/bash

cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
echo "Migrate..."
python manage.py makemigrations
python manage.py migrate
#./manage.py migrate --run-syncdb
