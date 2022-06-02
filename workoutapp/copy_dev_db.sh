#!/bin/bash

mongodump --archive="mongodump_prod_db" --db=django_workoutapp

mongorestore --archive="mongodump_prod_db" --nsFrom='django_workoutapp.*' --nsTo='django_workoutapp_dev.*'

rm mongodump_prod_db
