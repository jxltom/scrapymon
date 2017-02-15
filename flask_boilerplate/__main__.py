import os
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


def main(**kwargs):
    """Package entrypoint for running as server."""
    # Creat server.
    host = kwargs.get('host') or 'localhost'
    port = int(kwargs.get('port')) or 5000
    server = WSGIServer((host, port), app)

    # Logging.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.info('Running on http://{}:{}/'.format(
        server.server_host, server.server_port)
    )

    # Serve forever.
    server.serve_forever()


if __name__ == '__main__':
    main(port=(os.environ.get('PORT') or 5000))
