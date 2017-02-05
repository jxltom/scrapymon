from wsgi import worker
from flask_template import mail
from flask_mail import Message


@worker.task
def send_mail(**kwargs):
    """Send mail."""
    mail.send(Message(**kwargs))
    return 0


@worker.task
def async_test(x, y):
    """Celery test."""
    return x + y
