from . import login
from .form import LoginForm
from flask_login import login_user, current_user
from flask_template import login_manager
from flask_template.models.login_model import User
from flask import render_template, request, redirect, url_for, current_app


@login.route('/login', methods=['GET', 'POST'])
def login():
    """Log in and redirect to index page."""
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if _auth(email, password):
            user = User(id_=email)
            login_user(user, remember=True) if form.remember else login_user(user)
            next_url = request.args.get('next')
            return redirect(next_url or url_for('index.index'))

    return render_template('login.html', form=form)


@login_manager.user_loader
def user_loader(id_):
    return User(id_=id_)


def _auth(email, password):
    """Authentication for logging."""
    if current_app.config['LOGIN_EMAIL'] == email \
            and current_app.config['LOGIN_PASSWORD'] == password:
        return True
    return False

