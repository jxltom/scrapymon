"""
For using this, add flask_login.login_required decorator to your view functions.
"""

from flask import Blueprint

login = Blueprint('login', __name__)

from . import views
