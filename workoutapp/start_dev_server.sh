#!/bin/bash

source "../venv/bin/activate"

export DJANGO_SETTINGS_MODULE=workoutapp.dev_settings

python3 manage.py runserver 0.0.0.0:8080
