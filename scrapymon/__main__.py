import os
import argparse
import logging

from gevent.pywsgi import WSGIServer

from scrapymon.config import Config
from scrapymon.app import create_app, worker

app = create_app(Config(
    bootstrap=True,
    db=False,
    httpauth=True,
    mail=False,
    scheduler=False,
    auth=False,
    admin=False,
    index=True,
    wechat=False,
))


def main():
    """Convinent entrypoint for wrapper as script or exe."""
    # Convenient reference
    app_name = 'scrapymon'

    # Customized HelpFomatter without prefix.
    class CustomHelpFormatter(argparse.HelpFormatter):
        def add_usage(self, usage, actions, groups, prefix=''):
            super().add_usage(usage, actions, groups, prefix=prefix)

    # Application usage.
    usage_ = '\n'.join([
        'Usage: {} [--host=<host>] [--port=<port>] '
        '[--server=<address>] [--auth=<username:password>'.format(app_name),
        '',
        'Options:',
        '  --host      Default is 0.0.0.0',
        '  --port      Default is 5000',
        '  --server    Scrapyd server address with port. '
        'Default is http://127.0.0.1:6800',
        '  --auth      Username and passoword for http basic auth. '
        'Default is admin:admin',
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
    argparse_.add_argument(
        '--server', default=os.environ.get(
            'SCRAPYD_SERVER', 'Http://127.0.0.1:6800'))
    argparse_.add_argument('--auth', default='admin:admin')

    # Parse options.
    opts = argparse_.parse_args()
    host, port, help_ = opts.host, opts.port, opts.help
    scrapyd_server = opts.server
    basic_auth_username, basic_auth_password = opts.auth.split(':')

    # Print help information
    if help_:
        print(usage_)
        return

    # Update Scrapyd server address.
    app.config.update(SCRAPYD_SERVER=scrapyd_server)

    # Update http basic auth credential.
    app.config.update(BASIC_AUTH_USERNAME=basic_auth_username)
    app.config.update(BASIC_AUTH_PASSWORD=basic_auth_password)

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
