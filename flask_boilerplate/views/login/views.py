from flask import render_template, request, redirect, url_for
from flask_login import login_user, current_user, login_required

from flask_boilerplate import login_manager
from flask_boilerplate.models.user import User
from . import login
from .form import LoginForm


@login.route(login_manager.login_view_route, methods=['GET', 'POST'])
def log_in():
    """Login.

    If the function name is changed, make sure also changing the endpoint of
    login_view of login_manager.
    """
    if current_user.is_authenticated:
        return redirect(login_manager.success_redirect_url)

    form = LoginForm()
    if form.validate_on_submit():
        uid, pwd = form.username.data, form.password.data
        form.username.data, form.password.data = '', ''

        if _auth(uid, pwd):
            form.remember.data = True  # always enable remember me
            login_user(User(uid, pwd), remember=form.remember.data)

            return redirect(request.args.get('next') or
                            login_manager.success_redirect_url)

    return render_template('login.html', form=form)


@login_manager.user_loader
def _user_loader(uid):
    return User.query.get(uid)


def _auth(uid, pwd):
    """Authentication for login."""
    user = User.query.get(uid)
    if user and user.uid == uid and user.pwd == pwd:
        return True
    return False


@login.route('/login_required')
@login_required
def login_required():
    return 'success'
