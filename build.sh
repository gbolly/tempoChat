#!/usr/bin/env bash
# Exit on error
set -o errexit
python manage.py collectstatic --no-input
python manage.py migrate
