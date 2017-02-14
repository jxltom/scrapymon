web: gunicorn wsgi:app
worker: celery worker -A wsgi.worker --loglevel=info
service: scrapyd
