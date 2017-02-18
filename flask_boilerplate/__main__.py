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
        '  --host    Default is $HOST or 0.0.0.0 if $HOST is not defined',
        '  --port    Default is $PORT or 5000 if $PORT is not defined',
    ])

    # Initialzie argparse.
    argparse_ = argparse.ArgumentParser(
        prog=app_name, usage=usage_, add_help=False,
        formatter_class=CustomHelpFormatter)

    # Add arguments.
    # Default values are relavant environment variables or pre-defined values
    # This may cause problems if one has defined undesired environment variables
    # when running by default.
    argparse_.add_argument('--help', action='store_true', default=False)
    argparse_.add_argument('--host', default=os.environ.get('HOST', '0.0.0.0'))
    # Note that $PORT environment variable has to be used in Heroku.
    # Consider using $DYNO but it is subject to change or removal in Heroku.
    argparse_.add_argument(
        '--port', type=int, default=int(os.environ.get('PORT', 5000)))

    # Parse options.
    opts = argparse_.parse_args()
    host, port, help_ = opts.host, opts.port, opts.help

    # Print help information
    if help_:
        print(usage_)
        return

    # Creat server.
    server = WSGIServer((host, port), app)

    # Logging.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.info('{} is running on http://{}:{}/'.format(
        app_name, server.server_host, server.server_port)
    )

    # Serve forever.
    server.serve_forever()


if __name__ == '__main__':
    # Entrypoint for Heroku/Dokku/Flynn.
    main()
