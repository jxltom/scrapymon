from flask import request, redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user


class CustomIndexView(AdminIndexView):
    """Index view with authentication."""

    def is_accessible(self):
        """Authentication for views."""
        if current_user.is_authenticated:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        """Redirect for unauthenticated users."""
        return redirect(url_for('security.login', next=request.url))


class CustomModelView(ModelView):
    """Admin views with authentication"""
    can_delete = False
    can_edit = False
    column_searchable_list = ['id', 'email', 'password']
    column_editable_list = ['password']

    def is_accessible(self):
        """Authentication for views."""
        if current_user.is_authenticated:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        """Redirect for unauthenticated users."""
        return redirect(url_for('security.login', next=request.url))
