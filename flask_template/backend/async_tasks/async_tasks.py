from flask_template import worker
from flask_mail import Message


@worker.task
def send_mail(**kwargs):
    """Send mail by Flask-Mail."""
    from flask_template import mail
    mail.send(Message(**kwargs))
    return 0


@worker.task
def async_test(x, y):
    return x + y
