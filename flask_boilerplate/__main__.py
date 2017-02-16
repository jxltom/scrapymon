import os
import argparse
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
    """Convinent entrypoint for wrapper as script or exe."""
    # Convenient reference
    app_name = 'flask_boilerpalte'

    # Customized HelpFomatter without prefix.
    class CustomHelpFormatter(argparse.HelpFormatter):
        def add_usage(self, usage, actions, groups, prefix=''):
            super().add_usage(usage, actions, groups, prefix=prefix)

    # Application usage.
    usage_ = '\n'.join([
        'Usage: {} [--host=<host>] [--port=<port>]'.format(app_name),
        '',
        'Options:',
        '  --host    Default is 0.0.0.0',
        '  --port    Default is 5000',
    ])

    # Initialzie argparse.
    argparse_ = argparse.ArgumentParser(
        prog=app_name, usage=usage_, add_help=False,
        formatter_class=CustomHelpFormatter)

    # Add arguments.
    argparse_.add_argument('--help', action='store_true', default=False)
    argparse_.add_argument('--host', default='0.0.0.0')
    argparse_.add_argument('--port', type=int, default=5000)

    # Parse options.
    opts = argparse_.parse_args()
    host, port, help_ = opts.host, opts.port, opts.help

    # Overide port by $PORT environment variable in Heroku.
    # This may cause problems if one has defined PORT when running as script.
    # Consider using $DYNO but it is subject to change or removal in Heroku.
    port = int(os.environ.get('PORT', port))

    # Print help information
    if help_:
        print(usage_)
        return

    # Creat server.
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
    # Entrypoint for Heroku.
    main()
