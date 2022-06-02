#!/bin/bash

source "../venv/bin/activate"

export DJANGO_SETTINGS_MODULE=workoutapp.dev_settings

gunicorn -c config/gunicorn/dev.py
