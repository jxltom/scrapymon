from flask_boilerplate.config import Config
from flask_boilerplate.app import create_app

app = create_app(Config(
    bootstrap=True,
    db=True,
    httpauth=True,
    mail=True,
    scheduler=True,
    auth=True,
    admin=True,
    index=True,
    wechat=True,
))


def main():
    """Entrypoint for running application."""
    app.run()


if __name__ == '__main__':
    app.config.update(DEBUG=True)
    main()
