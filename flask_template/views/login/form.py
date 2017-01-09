from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        '', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(
        '', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')
