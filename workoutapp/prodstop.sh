#!/bin/bash

if [ -f "/var/run/gunicorn/prod.pid" ]; then
    pid=$(cat /var/run/gunicorn/prod.pid)
    echo $pid
    kill $pid
fi
