#!/bin/sh

./python_venv/bin/python manage.py migrate                  # Apply database migrations
./python_venv/bin/python manage.py collectstatic --noinput  # Collect static files

export DJANGO_SETTINGS_MODULE="catchpy.settings.aws"

# Start Gunicorn processes
echo Starting Gunicorn.
exec ./python_venv/bin/gunicorn -c catchpy/settings/gunicorn.conf.py catchpy.wsgi:application 