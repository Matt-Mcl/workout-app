#!/bin/bash

source "../venv/bin/activate"

export DJANGO_SETTINGS_MODULE=workoutapp.local_settings

python3 manage.py runserver
