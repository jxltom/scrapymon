from flask_login import UserMixin


class User(UserMixin):
    """User for logging."""
    def __init__(self, id_=None):
        self._id = id_

    def get_id(self):
        """Return unique id of user."""
        return self._id
