#!/usr/bin/env bash
# Exit on error
set -o errexit

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --no-input
exec "$@"
