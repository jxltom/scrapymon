web2: python flask_boilerplate/__main__.py
web: gunicorn flask_boilerplate.__main__:app
worker: celery worker -A flask_boilerplate.__main__.worker --loglevel=info
