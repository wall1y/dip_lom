from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, IPAddress, ValidationError, EqualTo, Email, Regexp
from app.dbase import User, Hosts

class HostAddForm(FlaskForm):
    hostname = StringField('Hostname', validators=[DataRequired(), Length(min=3, max=50)])
    ip = StringField('IP-address', validators=[DataRequired(),IPAddress()])
    os = StringField('OS', validators=[DataRequired(), Length(min=3, max=50)])
    submit = SubmitField('Add')

class UserAddForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EditorForm(FlaskForm):
    filename = StringField('Content', validators=[DataRequired(), Regexp(regex='^([a-zA-Z0-9\s\._-]+)$')])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save')

class NewFolderForm(FlaskForm):
    dirname = StringField('Content', validators=[DataRequired(), Regexp(regex='^([a-zA-Z0-9\s\._-]+)$')], render_kw={"placeholder": "Create new directory?"})
    submit = SubmitField('Create')