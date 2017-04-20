#-*- coding:utf-8 -*-
import pdb

from flask import render_template, request, session, redirect, url_for, flash

from ..models import IkrssUser, IkrssUserLog,IkrssRole,IkrssRssTag
from . import main
from .forms import UserRegisterForm
from .. import db


@main.before_app_first_request
def before_app_first_request():
    db.create_all()
    IkrssRole.insert_roles()
    IkrssRssTag.insert_tags()

@main.route('/')
@main.route('/index')
def index():
    user_agent = request.headers.get('User-Agent', '')
    return render_template("index.html", name=user_agent)


@main.route('/user/<name>')
def user(name):
    return "Heelo, %s" % name



