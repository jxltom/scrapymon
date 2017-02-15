import logging

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


def main():
    """Package entrypoint for running as server."""
    # Creat server.
    server = WSGIServer(('127.0.0.1', 5000), app)

    # Logging.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.info('Running on http://{}:{}/'.format(
        server.server_host, server.server_port)
    )

    # Serve forever.
    server.serve_forever()


if __name__ == '__main__':
    main()
