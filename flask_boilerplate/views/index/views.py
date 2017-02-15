from flask import render_template
from flask_security import login_required

from . import index


@index.route('/_')
def index_test():
    return None


@index.route('/_auth')
@login_required
def login_required_test():
    return 'success'
