#-*- coding:utf-8 -*-
import pdb

from flask import render_template, request, session, redirect, url_for, flash

from ..models import IkssUser, IkssUserLog,IkssRole
from . import auth
from .forms import RegisterForm,LoginForm
from .. import db


@auth.route('/user/<name>')
def user(name):
    return "Heelo, %s" % name




@auth.route('/login', methods=['GET', 'POST'])
def login():
    name = None
    form = LoginForm()
    return render_template('auth/login.html',form=form,name=name)



@auth.route('/register/', methods=['GET', 'POST'])
def register():
    print("Method1:" + request.method)
    form = RegisterForm()
    if form.validate_on_submit():
        #用户名是否已经存在
        if IkssUser.query.filter_by(username=form.username.data) is not None:
            flash("用户名已经存在，请重新输入")
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
        "register.html", form=form, name=session.get('name'))

