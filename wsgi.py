from config import Config
from scrapymon import create_app, worker

app = create_app(Config(
    bootstrap=True,
    db=True,
    httpauth=True,
    mail=False,
    scheduler=False,
    auth=False,
    admin=False,
    index=True,
    wechat=False,
))

if __name__ == '__main__':
    app.config.update(DEBUG=True)
    app.run()
