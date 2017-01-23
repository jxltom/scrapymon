from . import login
from .form import LoginForm
from flask_login import login_user, current_user, login_required
from flask_template import login_manager
from flask_template.models.login_model import User
from flask import render_template, request, redirect, url_for, current_app

REDIRECT_URL_ON_SUCCESS = '/'


@login.route(login_manager.LOGIN_VIEW_ROUTE, methods=['GET', 'POST'])
def log_in():
    """
    Log in and redirect to REDIRECT_URL_ON_SUCCESS. If the function name is
    changed, make sure also changing the endpoint of login_view of
    login_manager.
    """
    if current_user.is_authenticated:
        return redirect(REDIRECT_URL_ON_SUCCESS)

    form = LoginForm()
    if form.validate_on_submit():
        username, password = form.username.data, form.password.data
        form.username.data, form.password.data = '', ''

        if _auth(username, password):
            # enable remember me
            form.remember.data = True

            login_user(User(id_=username), remember=form.remember.data)
            return redirect(request.args.get('next') or REDIRECT_URL_ON_SUCCESS)

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

