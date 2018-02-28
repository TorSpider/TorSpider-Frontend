from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import StringField, PasswordField


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    invitecode = StringField('Invite Code', [validators.DataRequired()])
