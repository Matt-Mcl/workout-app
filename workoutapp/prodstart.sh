source "../venv/bin/activate"

gunicorn -c config/gunicorn/prod.py