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


def main(*args, **kwargs):
    """Package entrypoint."""
    print(args, kwargs)
    # Creat server.
    host = kwargs.get('host', '0.0.0.0')
    port = int(kwargs.get('port', 5000))
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
    # Using $PORT in Heroku, otherwise using 5000 as default.
    main(port=(os.environ.get('PORT', 5000)))
