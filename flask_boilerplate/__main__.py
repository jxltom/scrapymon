from gevent.pywsgi import WSGIServer

from flask_boilerplate.config import Config
from flask_boilerplate.app import create_app, worker

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


def serve_app():
    """Package entrypoint for running as server."""
    WSGIServer(('', 5000), app).serve_forever()


if __name__ == '__main__':
    serve_app()
