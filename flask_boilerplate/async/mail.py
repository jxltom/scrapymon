from flask_mail import Message

from flask_boilerplate import mail
from flask_boilerplate import worker


@worker.task
def send_mail(**kwargs):
    """Send mail."""
    mail.send(Message(**kwargs))
    return 0


@worker.task
def flask_security_send_mail(msg):
    mail.send(msg)
    return 0


@worker.task
def async_test(x, y):
    """Celery test."""
    return x + y
