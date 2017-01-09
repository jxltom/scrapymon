from flask import Blueprint

main = Blueprint('index', __name__)

from . import views