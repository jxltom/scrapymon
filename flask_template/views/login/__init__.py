from flask import Blueprint

login = Blueprint('login', __name__)

from . import views


"""
This modules depends on bootstrap. You need to set the correct dependence
in the config.py.
"""