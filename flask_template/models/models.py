from flask_template import db
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id_=None):
        self._id = id_

    def get_id(self):
        return self._id
