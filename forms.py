from re import S
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, IPAddress


class HostAddForm(FlaskForm):
    hostname = StringField('Hostname', validators=[DataRequired(), Length(min=3, max=50)])
    ip = StringField('IP-address', validators=[DataRequired(),IPAddress()])
    submit = SubmitField('Add')