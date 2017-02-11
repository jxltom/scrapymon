from flask_admin.contrib.sqla import ModelView


class UserView(ModelView):
    can_delete = False
    can_edit = False
    column_searchable_list = ['id', 'email', 'password']
    column_editable_list = ['password']
