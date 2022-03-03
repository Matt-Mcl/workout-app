bash ./prodstop.sh > /dev/null

source "../venv/bin/activate"

sudo mkdir -pv /var/{log,run}/gunicorn/ > /dev/null
sudo chown -cR ubuntu:ubuntu /var/{log,run}/gunicorn/

gunicorn -c config/gunicorn/prod.py
