from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField,PasswordField,BooleanField
from wtforms.validators import Email,DataRequired,EqualTo,Regexp,Length
from wtforms import ValidationError
from ..models import IkrssUser


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(1,24),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                   'Usernames must have only letters, '                                                                 'numbers, dots or underscores')])
    password = PasswordField('password', validators=[DataRequired(),EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(),DataRequired(),Length(1,64)])

    submit = SubmitField('Register')

    def validate_email(self, field):
        if IkrssUser.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if IkrssUser.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    is_remember = BooleanField("remember me")

    submit = SubmitField('Submit')
