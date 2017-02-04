from flask_template import worker


@worker.task
def celery_test(x, y):
    return x + y
