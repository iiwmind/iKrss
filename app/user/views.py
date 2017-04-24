#-*- coding:utf-8 -*-
import pdb

from flask import render_template, request, session, redirect, url_for, flash,current_app

from ..models import IkrssUser, IkrssUserLog,IkrssRole
from ..email import send_email
from . import user
from .forms import RegisterForm,LoginForm
from .. import db
from flask_login import login_required,login_user,logout_user,current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_required
@user.route('/profile')
def profile(name):
    return "Heelo, %s" % name






@user.route('/subscribe')
@login_required
def subscribe():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('auth.confirmtips'))







