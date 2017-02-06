from config import Config
from flask_template import create_app, worker

app = create_app(Config(
    bootstrap=True,
    db=True,
    scheduler=True,
    mail=True,
    index=True,
    login=True,
    wechat=True,
))

if __name__ == '__main__':
    app.config.update(DEBUG=True)
    app.run()
