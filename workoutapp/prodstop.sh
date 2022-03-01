pid=$(cat /var/run/gunicorn/prod.pid)
echo $pid
kill $pid
