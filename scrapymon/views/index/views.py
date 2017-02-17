from collections import OrderedDict
import json

from flask import render_template, flash, current_app
from flask_security import login_required
from werkzeug.local import LocalProxy
import requests

from . import index

# Convenient reference to scrapyd server.
scrapyd_server = LocalProxy(lambda: current_app.config['SCRAPYD_SERVER'])
# Convenient reference to debug setting.
debug = LocalProxy(lambda: current_app.config['DEBUG'])

# Endpoints of scrapyd API.
listprojects_url = '/listprojects.json'
listspiders_url = '/listspiders.json'
listversions_url = '/listversions.json'
listjobs_url = '/listjobs.json'
schedule_url = '/schedule.json'


@index.errorhandler(requests.ConnectionError)
def server_connection_error(e):
    """Flash messages if server can not be connected."""
    if debug:
        flash(e.args, 'danger')

    flash(
        'The connection to Scrapyd server can not be established. '
        'Please check status of Scrapyd server in {}.'.format(scrapyd_server),
        'danger'
    )
    return render_template('index/error.html')


@index.route('/')
def projects_dash():
    """Projects view."""
    projects = OrderedDict()

    # Get projects as well as their versions, spiders
    for project in _list_projects():
        spiders = _list_spiders(project)
        versions = _list_versions(project)
        projects[project] = dict(versions=versions, spiders=spiders)

    return render_template('index/projects.html', projects=projects)


@index.route('/jobs')
def jobs_dash():
    """Jobs view."""
    jobs = OrderedDict()
    jobs['pending'], jobs['running'], jobs['finished'] = [], [], []

    # Get jobs and sort them as pending, running and finished.
    for project in _list_projects():
        pending_jobs, running_jobs, finished_jobs = _list_jobs(project)

        for job in pending_jobs:
            job['project'] = project
            jobs['pending'].append(job)

        for job in running_jobs:
            job['project'] = project
            jobs['running'].append(job)

        for job in finished_jobs:
            job['project'] = project
            jobs['finished'].append(job)

    return render_template('index/jobs.html', jobs=jobs)


@index.route('/schedule/<project>/<spider>')
def schedule(project, spider):
    """Schedule spider run."""
    # Run spider and get response from server.
    url = scrapyd_server + schedule_url
    raw = requests.post(url, params=dict(project=project, spider=spider)).text
    r = json.loads(raw)

    # Parse response
    status, node_name = r.get('status', ''), r.get('node_name', '')
    jobid = r.get('jobid', '')

    # Flash messages.
    if status != 'ok':
        flash(
            'Can not run spider {} in project {} in node {}. '
            'The raw message returned by Scrapyd server is {}'.format(
                spider, project, node_name, raw), 'warning'
        )
    else:
        flash(
            'Run spider {} in project {} in node {} successfully. '
            'The job ID is {}'.format(
                spider, project, node_name, jobid), 'success'
        )

    return 'success'


def _list_projects():
    """Get projects list."""
    # Get response from server.
    raw = requests.get(scrapyd_server + listprojects_url).text
    r = json.loads(raw)

    # Parse response.
    status, node_name = r.get('status', ''), r.get('node_name', '')
    projects = r.get('projects', [])

    # Flash error messages.
    if status != 'ok':
        flash(
            'Can not get projects in node {}. '
            'The raw message returned by Scrapyd server is {}'.format(
                node_name, raw), 'warning'
        )

    # Return projects list.
    return projects


def _list_versions(project):
    """Get versions list of a project"""
    # Get response from server
    raw = requests.get(scrapyd_server + listversions_url,
                       params=dict(project=project)).text
    r = json.loads(raw)

    # Parse response.
    status, node_name = r.get('status', ''), r.get('node_name', '')
    versions = r.get('versions', [])

    # Flash error messages.
    if status != 'ok':
        flash(
            'Can not get versions of project {} in node {}. '
            'The raw message returned by Scrapyd server is {}'.format(
                project, node_name, raw), 'warning'
        )

    # Return versions list.
    return versions


def _list_spiders(project):
    """Get spiders list of a project"""
    # Get response from server
    raw = requests.get(scrapyd_server + listspiders_url,
                       params=dict(project=project)).text
    r = json.loads(raw)

    # Parse response.
    status, node_name = r.get('status', ''), r.get('node_name', '')
    spiders = r.get('spiders', [])

    # Flash error messages.
    if status != 'ok':
        flash(
            'Can not get spiders of project {} in node {}. '
            'The raw message returned by Scrapyd server is {}'.format(
                project, node_name, raw), 'warning'
        )

    # Return spiders list.
    return spiders


def _list_jobs(project):
    """Get jobs list of a project."""
    # Get response from server.
    raw = requests.get(scrapyd_server + listjobs_url,
                       params=dict(project=project)).text
    r = json.loads(raw)

    # Parse response.
    status, node_name = r.get('status', ''), r.get('node_name', '')
    pending_jobs = r.get('pending', [])
    running_jobs = r.get('running', [])
    finished_jobs = r.get('finished', [])

    # Flash error messages.
    if status != 'ok':
        flash(
            'Can not get jobs of project {} in node {}. '
            'The raw message returned by Scrapyd server is {}'.format(
                project, node_name, raw), 'warning'
        )

    return pending_jobs, running_jobs, finished_jobs


@index.route('/_')
def index_test():
    return render_template('base.html')


@index.route('/_auth')
@login_required
def login_required_test():
    return 'success'
