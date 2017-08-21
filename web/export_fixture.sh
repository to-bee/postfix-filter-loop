#!/usr/bin/env bash

cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

#./migrate.sh

echo "Export fixture..."
./manage.py dumpdata --format json --indent 2 --exclude admin.logentry --exclude sessions.session > fixture.json
# --exclude contenttypes
