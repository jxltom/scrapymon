from config import Config
from flask_template import create_app, create_worker

app = create_app(Config(
    bootstrap=True,
    db='sqlite://',
    scheduler=True,
    mail=True,
    index=True,
    login=True,
    wechat=True,
))
worker = create_worker(app)
from flask_template.backend.async_tasks.async_tasks import send_mail

if __name__ == '__main__':
    app.config.update(DEBUG=True)
    app.run()
