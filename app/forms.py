from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from wtforms import validators
from wtforms.fields import StringField, BooleanField, SelectMultipleField, PasswordField, SelectField
from app import db

# Required for WTForms-Alchemy to work with Flask-WTF
BaseModelForm = model_form_factory(FlaskForm, strip_string_fields=True)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    invitecode = StringField('Invite Code', [validators.DataRequired()])
