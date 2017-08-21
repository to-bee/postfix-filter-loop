#!/usr/bin/env bash

cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ssh -t root@86.119.36.67 "docker exec -it ip6_django_1 ./web/manage.py dumpdata --format json --indent 2 --exclude admin.logentry --exclude sessions.session > /var/ip6.backend/generated/fixture.json"

FIXTURE_PATH="/var/ip6.backend/generated/fixture.json"
scp -r root@ip6:$FIXTURE_PATH ./
ls -l