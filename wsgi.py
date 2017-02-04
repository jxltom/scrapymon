from config import Config
from flask_template import create_app

app = create_app(Config(
    bootstrap=True,
    db='sqlite://',
    scheduler=True,
    index=True,
    login=True,
    wechat=True,
))
from flask_template import worker

if __name__ == '__main__':
    app.config.update(DEBUG=True)
    app.run()
