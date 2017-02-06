web: gunicorn wsgi:app
worker: celery worker -A flask_template.worker --loglevel=info
