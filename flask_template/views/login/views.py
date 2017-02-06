from flask_template.views.login import login
from flask_template.views.login.form import LoginForm
from flask_template.models.user import User
from flask_template import login_manager
from flask_login import login_user, current_user, login_required
from flask import render_template, request, redirect, url_for


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
        id, pwd = form.username.data, form.password.data
        form.username.data, form.password.data = '', ''

        if _auth(id, pwd):
            form.remember.data = True  # always enable remember me
            login_user(User(id, pwd), remember=form.remember.data)

            return redirect(request.args.get('next') or
                            login_manager.success_redirect_url)

    return render_template('login.html', form=form)


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


def _auth(id, pwd):
    """Authentication for login."""
    user = User.query.get(id)
    if user and user.id == id and user.pwd == pwd:
        return True
    return False


@login.route('/login_required')
@login_required
def login_required():
    return 'success'
