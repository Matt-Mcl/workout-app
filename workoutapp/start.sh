#!/bin/bash

python3 manage.py migrate

python3 manage.py collectstatic --noinput

gunicorn -b 0.0.0.0:8007 workoutapp.wsgi:application --log-level=debug --error-logfile=/app/error.log --access-logfile=/app/error.log
