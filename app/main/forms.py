from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField,PasswordField
from wtforms.validators import Required,Email,DataRequired


class UserRegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])


    submit = SubmitField('Submit')

