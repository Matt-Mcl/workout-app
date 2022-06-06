#!/bin/bash

sudo -u postgres dropdb django_workoutapp_dev
sudo -u postgres createdb django_workoutapp_dev -T django_workoutapp
