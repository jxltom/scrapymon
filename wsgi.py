from config import Config
from flask_boilerplate import create_app, worker

app = create_app(Config(
    bootstrap=True,
    db=True,
    httpauth=False,
    mail=True,
    scheduler=True,
    index=False,
    login=False,
    wechat=False,
))

if __name__ == '__main__':
    app.config.update(DEBUG=True)
    app.run()
