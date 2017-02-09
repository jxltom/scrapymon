from . import index
from flask_security import login_required
from flask import render_template


@index.route('/_')
def index_test():
    return 'success'


@index.route('/___')
@login_required
def login_required_test():
    return render_template('index.html')
