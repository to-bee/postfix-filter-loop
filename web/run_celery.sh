#!/bin/bash

# Runs celery-beat - this will only schedule tasks
#celery -A backend beat --loglevel info -S django &

# Runs the worker - this will executed tasks
#celery -A backend worker --loglevel info -f celery.log

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DJANGO_SETTINGS_MODULE="backend.settings_docker"

osascript -e 'tell application "Terminal" to do script "cd '$DIR' && source '$VIRTUAL_ENV'/bin/activate && celery -A backend beat --loglevel info -S django"'
osascript -e 'tell application "Terminal" to do script "cd '$DIR' && source '$VIRTUAL_ENV'/bin/activate && celery -A backend worker --loglevel info -f /var/ip6.backend/celery.log"'

lsof -P | grep ':6379' | awk '{print $2}' | xargs kill -9
osascript -e 'tell application "Terminal" to do script "redis-server"'