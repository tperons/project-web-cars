#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python /app/manage.py collectstatic --noinput

WORKERS=${GUNICORN_WORKERS:-$((2 * $(nproc) + 1))}
export WORKERS

exec gunicorn core.wsgi --bind 0.0.0.0:8000 --workers "$WORKERS" --chdir=/app
