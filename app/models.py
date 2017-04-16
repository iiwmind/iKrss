#-*- coding=utf-8 -*-
#from sqlalchemy import Column,Integer,String
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import db,login_manager

class IkssRole(db.Model):
    __tablename__ = "ikss_roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(20), unique=True, index=True)

    ikssusers = db.relationship(
        'IkssUser', backref='ikssrole', lazy="dynamic")

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return '<IkssRole %r>' % self.role_name


class IkssUser(db.Model, UserMixin):
    __tablename__ = "ikss_users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(30))
    password_hash=db.Column(db.String(256))
    email = db.Column(db.String(30))
    date = db.Column(db.Date, default=datetime.now().date(), index=True)
    time = db.Column(db.Time, default=datetime.now().time())
    active_flag = db.Column(db.Boolean, default=True)

    ikssrole_id = db.Column(db.Integer, db.ForeignKey('ikss_roles.id'))

    ikssuser_logs = db.relationship(
        'IkssUserLog', backref='ikssuser', lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("不能直接get密码")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __init__(self, username, password, email,role):
        self.username = username
        self.password = password
        self.email = email
        self.ikssrole_id = role

    def __repr__(self):
        return '<IkssUser %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return IkssUser.query.get(int(user_id))


class IkssUserLog(db.Model):
    __tablename__ = "ikss_users_log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ikssuser_id=db.Column(db.Integer,db.ForeignKey('ikss_users.id'))
    date = db.Column(db.Date, default=datetime.now().date(), index=True)
    time = db.Column(db.Time, default=datetime.now().time())
    type = db.Column(db.String(4))

    def __init__(self, type,user):
        self.type = type
        self.ikssuser_id = user
