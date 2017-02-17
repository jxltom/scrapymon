web: python scrapymon/__main__.py --auth=test:test
worker: celery worker -A scrapymon.__main__.worker --loglevel=info
service: scrapyd
