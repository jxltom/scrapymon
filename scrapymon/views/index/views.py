import json

from flask import render_template, flash, current_app
from flask_security import login_required
from werkzeug.local import LocalProxy
import requests

from . import index

# Convenient reference to scrapyd server.
server = LocalProxy(lambda: current_app.config['SCRAPYD_SERVER'])
# Convenient reference to debug setting.
debug = LocalProxy(lambda: current_app.config['DEBUG'])

# Endpoints of scrapyd API.
listprojects = '/listprojects.json'
listspiders = '/listspiders.json'
listversions = '/listversions.json'


@index.errorhandler(requests.ConnectionError)
def server_connection_error(e):
    """Flash messages if server can not be connected."""
    if debug:
        flash(e.args, 'danger')
    flash('The connection to Scrapyd server can not be established.'
          'Please check Scrapyd status in local host.')
    return render_template('index/error.html')


@index.route('/')
def projects_dash():
    """Projects view."""
    projects = {}

    # Get projects as well as their versions, spiders
    for project in _list_projects():
        spiders = _list_spiders(project)
        versions = _list_versions(project)
        projects[project] = dict(versions=versions, spiders=spiders)

    return render_template('index/projects.html', projects=projects)


def _list_projects():
    """Get projects list."""
    # Get response from server.
    raw = requests.get(server + listprojects).text
    r = json.loads(raw)

    # Parse response.
    status, node_name = r.get('status', ''), r.get('node_name', '')
    projects = r.get('projects', [])

    # Flash error messages.
    if status != 'ok':
        flash(
            'Can not get projects in node {}. '
            'The raw message returned by Scrapyd server is {}'.format(
                node_name, raw), 'danger'
        )

    # Return projects list.
    return projects


def _list_spiders(project):
    """Get spiders list of a project"""
    # Get response from server
    raw = requests.get(server + listspiders, params=dict(project=project)).text
    r = json.loads(raw)

    # Parse response.
    status, node_name = r.get('status', ''), r.get('node_name', '')
    spiders = r.get('spiders', [])

    # Flash error messages.
    if status != 'ok':
        flash(
            'Can not get spiders of project {} in node {}. '
            'The raw message returned by Scrapyd server is {}'.format(
                project, node_name, raw), 'danger'
        )

    # Return projects list.
    return spiders


def _list_versions(project):
    """Get versions list of a project"""
    # Get response from server
    raw = requests.get(server + listversions, params=dict(project=project)).text
    r = json.loads(raw)

    # Parse response.
    status, node_name = r.get('status', ''), r.get('node_name', '')
    versions = r.get('versions', [])

    # Flash error messages.
    if status != 'ok':
        flash(
            'Can not get versions of project {} in node {}. '
            'The raw message returned by Scrapyd server is {}'.format(
                project, node_name, raw), 'danger'
        )

    # Return projects list.
    return versions


@index.route('/jobs')
def jobs_dash():
    """Jobs view."""
    return render_template('index/jobs.html')


@index.route('/_')
def index_test():
    return render_template('base.html')


@index.route('/_auth')
@login_required
def login_required_test():
    return 'success'
