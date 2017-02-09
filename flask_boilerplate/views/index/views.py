from flask_security import login_required

from . import index


@index.route('/_')
def index_test():
    return 'success'


@index.route('/_login_required')
@login_required
def login_required_test():
    return 'success'
