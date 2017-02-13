from flask_security import UserMixin, RoleMixin

from scrapymon import db

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
)


class Role(db.Model, RoleMixin):
    """Role table."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        """Return name attribute as foreign key."""
        return self.name


class User(db.Model, UserMixin):
    """User table."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)

    confirmed_at = db.Column(db.DateTime)

    last_login_ip = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime)
    current_login_ip = db.Column(db.String(255))
    current_login_at = db.Column(db.DateTime)
    login_count = db.Column(db.Integer)

    roles = db.relationship(
        'Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )
