from flask import current_app
from flask import (render_template, request, redirect, url_for)
from flask_login import login_user, current_user

from flask_template.models.models import User
from flask_template import login_manager
from . import login
from .form import LoginForm


@login.route('/login', methods=['GET', 'POST'])
def login():
    """Log in and redirect to index page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit() \
            and form.username.data == current_app.config['USERNAME'] \
            and form.password.data == current_app.config['PASSWORD']:
        user = User(id_=form.username.data)
        login_user(user, remember=True) if form.remember else login_user(user)
        next_url = request.args.get('next')
        return redirect(next_url or url_for('main.index'))
    return render_template('login.html', form=form)


@login_manager.user_loader
def user_loader(id_):
    return User(id_=id_)

