#!/bin/bash

# Delete existing jobs
celery -A backend purge -f

# Runs celery-beat - this will only schedule tasks
celery -A backend beat --loglevel debug -S django &

# Runs the worker - this will executed tasks
celery -A backend worker --loglevel debug -f /var/ip6.backend/celery.log &