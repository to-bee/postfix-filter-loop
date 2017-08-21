#!/usr/bin/env bash

cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

#./migrate.sh

echo "Load fixture..."
manage.py loaddata fixture.json

migrate.sh