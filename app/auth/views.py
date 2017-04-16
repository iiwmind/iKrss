#-*- coding:utf-8 -*-
import pdb

from flask import render_template, request, session, redirect, url_for, flash

from ..models import IkssUser, IkssUserLog,IkssRole
from . import auth
from .forms import RegisterForm,LoginForm
from .. import db
from flask_login import login_required,login_user,logout_user


@login_required
@auth.route('/user/<name>')
def user(name):
    return "Heelo, %s" % name




@auth.route('/login', methods=['GET', 'POST'])
def login():
    name = None
    form = LoginForm()
    if form.validate_on_submit():
        user = IkssUser.query.filter_by(username=form.username.data)
        if user is not None and user.verfy_password(form.password.data):
            login_user(form.is_remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

    return render_template('auth/login.html',form=form,name=name)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出')
    return redirect(url_for('main.index'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    db.create_all()
    #print("Method1:" + request.method)
    form = RegisterForm()
    if form.validate_on_submit():
        #用户名是否已经存在
        if IkssUser.query.filter_by(username=form.username.data).first() is not None:
            flash("用户名:%s 已经存在，请重新输入"% form.username.data)
            return redirect(url_for('.register'))

        role = IkssRole.query.all()[0]
        user = IkssUser(form.username.data,form.password.data,form.email.data, role.id)

        db.session.add(user)
        db.session.commit()

        user_log = IkssUserLog("C",user.id)
        db.session.add(user_log)
        flash("用户已经切换!")
        session['username'] = form.username.data
        return redirect(url_for('.register'))
    return render_template(
        "auth/register.html", form=form, name=session.get('name'))

