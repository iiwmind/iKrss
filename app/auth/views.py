#-*- coding:utf-8 -*-
import pdb

from flask import render_template, request, session, redirect, url_for, flash,current_app

from ..models import IkrssUser, IkrssUserLog,IkrssRole
from ..email import send_email
from . import auth
from .forms import RegisterForm,LoginForm
from .. import db
from flask_login import login_required,login_user,logout_user,current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_required
@auth.route('/user/<name>')
def user(name):
    return "Heelo, %s" % name


@auth.before_app_request
def before_request():
    #print(type(request))
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint is not None\
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)

    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('auth.confirmtips'))

@auth.route('/confirmtotips')
@login_required
def confirmtips():
    if  current_user.confirmed:
        return redirect(url_for('main.index'))
    #token = current_user.generate_confirmation_token()
    #send_email(current_user.email, 'Confirm Your Account',
    #          'auth/email/confirm', user=current_user, token=token)
    #flash('A new confirmation email has been sent to you by email.')
    return render_template(
     "auth/confirmtips.html", name=session.get('name'))
    #return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('auth.resend_confirmation'))
    return redirect(url_for('main.index'))






@auth.route('/login', methods=['GET', 'POST'])
def login():
    name = None
    error = None
    #如果用户已经登陆呢
    #if current_user.is_authenticated:
    #    return redirect(request.args.get('next') or url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = IkrssUser.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.is_remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            error ="用户名不存在或者密码错误"

    return render_template('auth/login.html',form=form,name=name,error=error)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出')
    return redirect(url_for('main.index'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and not current_user.confirmed:
        return render_template('auth/unconfirmed.html')
    elif current_user.is_authenticated and  current_user.confirmed:
        return redirect(url_for('main.index'))

    #print("Method1:" + request.method)
    form = RegisterForm()
    if form.validate_on_submit():
        #用户名是否已经存在
        if IkrssUser.query.filter_by(username=form.username.data).first() is not None:
            flash("用户名: %s  已经存在，请重新输入"% form.username.data)
            return redirect(url_for('.register'))

        user = IkrssUser(form.username.data, form.password.data, form.email.data)
        #pdb.set_trace()

        db.session.add(user)
        db.session.commit()

        user_log = IkrssUserLog("C",user.id)
        db.session.add(user_log)

        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account','auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        session['username'] = form.username.data
        #return redirect(url_for('.register'))
        return render_template(
        "auth/confirmtips.html", name=session.get('name'))
    return render_template(
        "auth/register.html", form=form, name=session.get('name'))





