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


if __name__ == '__main__':
    app.config.update(DEBUG=True)
    app.run()
