from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField,PasswordField,BooleanField
from wtforms.validators import Email,DataRequired


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])


    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    is_remember = BooleanField("remember me")

    submit = SubmitField('Submit')
