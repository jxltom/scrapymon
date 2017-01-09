from flask_login import UserMixin


class User(UserMixin):
    """Simple user class for logging."""
    def __init__(self, id_=None):
        self._id = id_

    def get_id(self):
        """Return the unique id of a user."""
        return self._id
