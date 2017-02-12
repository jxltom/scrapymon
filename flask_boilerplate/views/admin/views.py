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


class UserModelView(ModelView):
    """Admin views with authentication"""
    can_create = True
    can_delete = True
    can_edit = True
    can_export = True
    can_view_details = True
    can_set_page_size = True

    edit_modal = False
    create_modal = False

    column_display_pk = True
    column_display_all_relations = True
    column_auto_select_related = True

    column_searchable_list = ['email', ]
    column_editable_list = ['email', 'password', 'active']
    column_exclude_list = ['password']
    column_filters = ['active']

    form_excluded_columns = ['active']

    def is_accessible(self):
        """Authentication for views."""
        if current_user.is_authenticated:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        """Redirect for unauthenticated users."""
        return redirect(url_for('security.login', next=request.url))


class RoleModelView(ModelView):
    """Admin views with authentication"""
    can_create = True
    can_delete = True
    can_edit = True
    can_export = True
    can_view_details = True
    can_set_page_size = True

    edit_modal = False
    create_modal = False

    column_display_pk = True
    column_auto_select_related = True

    column_searchable_list = ['name', 'description']
    column_editable_list = ['name', 'description']
    column_filters = ['name']

    def is_accessible(self):
        """Authentication for views."""
        if current_user.is_authenticated:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        """Redirect for unauthenticated users."""
        return redirect(url_for('security.login', next=request.url))