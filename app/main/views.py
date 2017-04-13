import pdb

from flask import render_template, request, session, redirect, url_for, flash

from ..models import IkssUser, IkssUserLog
from . import main
from .forms import UserRegisterForm
from .. import db


@main.route('/')
@main.route('/index')
def index():
    user_agent = request.headers.get('User-Agent', '')
    return render_template("user.html", name=user_agent)


@main.route('/user/<name>')
def user(name):
    return "Heelo, %s" % name


@main.route('/register/', methods=['GET', 'POST'])
def register():
    print("Method:" + request.method)
    form = UserRegisterForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:

            #测试创建用户
            user_log = IkssUserLog("C")
            user = IkssUser("iiw","1234","iiw@126.com")
            pdb.set_trace()
            db.session.add(user_log)
            db.session.add(user)
            flash("用户已经切换!")
        session['name'] = form.name.data
        return redirect(url_for('.register'))
    return render_template(
        "register.html", form=form, name=session.get('name'))

