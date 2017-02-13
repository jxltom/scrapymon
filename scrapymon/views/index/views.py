from flask import render_template, flash, current_app, g
from flask_security import login_required
from werkzeug.local import LocalProxy
import requests

from . import index


# Convenient reference to scrapyd server.
server = LocalProxy(lambda: current_app.config['SCRAPYD_SERVER'])

# Endpoints of scrapyd API.
listprojects = '/listprojects.json'


@index.errorhandler(requests.ConnectionError)
def server_connection_error(e):
    """Flash messages if server can not be connected."""
    flash(e.args, 'danger')
    return render_template('index/error.html')


@index.route('/')
def projects():
    """Projects view."""
    return render_template('index/projects.html')


@index.route('/jobs')
def jobs():
    """Jobs view."""
    return render_template('index/jobs.html')


@index.route('/listprojects')
def list_projects():
    return requests.get(server + listprojects).text


@index.route('/_')
def index_test():
    return render_template('base.html')


@index.route('/_auth')
@login_required
def login_required_test():
    return 'success'
