"""
For using this, add flask_login.login_required decorator to your view functions.
Bootstrap and database are automatically enabled for using this module. Note
that you have to provide appropriate settings for database in DBConfig.
"""

from flask import Blueprint

login = Blueprint('login', __name__)

from . import views
