from tokenize import group
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, IPAddress, ValidationError, EqualTo, Email, Regexp
from app.dbase import User, Hosts

class HostAddForm(FlaskForm):
    hostname = StringField('Имя узла', validators=[DataRequired(), Length(min=3, max=50)])
    ip = StringField('IP-адрес', validators=[DataRequired(),IPAddress()])
    os = StringField('ОС', validators=[DataRequired(), Length(min=3, max=50)])
    group = SelectField('Группа', validators=[DataRequired()])
    playbooks = SelectMultipleField('Плейбуки', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Добавить')

class GroupAddForm(FlaskForm):
    group_name = StringField('Имя группы', validators=[DataRequired(), Length(min=3, max=50)])
    playbooks = SelectMultipleField('Плейбуки', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Добавить')

class UserAddForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите Пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Добавить')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже занято. Используйте другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Такой email уже занят. Используйте другой.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Запомнить')
    submit = SubmitField('Войти')

class EditorForm(FlaskForm):
    filename = StringField('Имя файла', validators=[DataRequired(), Regexp(regex='^([a-zA-Z0-9\s\._-]+)$')])
    content = TextAreaField('Содержимое', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

