from . import login
from .form import LoginForm
from flask_login import login_user, current_user, login_required
from flask_template import login_manager
from flask_template.models.login_model import User
from flask import render_template, request, redirect, url_for, current_app


@login.route('/login', methods=['GET', 'POST'])
def log_in():
    """Log in and redirect to index page."""
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if _auth(username, password):
            user = User(id_=username)
            login_user(user, remember=True) if form.remember else login_user(user)
            next_url = request.args.get('next')
            return redirect(next_url or url_for('index.index'))

    return render_template('login.html', form=form)


@login_manager.user_loader
def user_loader(id_):
    return User(id_=id_)


def _auth(username, password):
    """Authentication for logging."""
    if current_app.config['LOGIN_USERNAME'] == username \
            and current_app.config['LOGIN_PASSWORD'] == password:
        return True
    return False


@login.route('/login_required')
@login_required
def login_required():
    return 'logged in'

