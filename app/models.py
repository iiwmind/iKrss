# -*- coding=utf-8 -*-
# from sqlalchemy import Column,Integer,String
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db, login_manager


class Permission:
    SEND = 0x01
    AUTOSEND = 0x02
    # WRITE_ARTICLES = 0x04
    # MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class IkrssRole(db.Model):
    __tablename__ = "ikrss_roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True)

    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    ikrss_users = db.relationship(
        'IkrssUser', backref='ikrss_role', lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<IkrssRole %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.SEND, True),
            'VIPUser': (Permission.SEND | Permission.AUTOSEND, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = IkrssRole.query.filter_by(name=r).first()
            if role is None:
                role = IkrssRole(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class IkrssUser(db.Model, UserMixin):
    __tablename__ = "ikrss_users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(30))
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(30))
    date = db.Column(db.Date, default=datetime.now().date(), index=True)
    time = db.Column(db.Time, default=datetime.now().time())
    active_flag = db.Column(db.Boolean, default=True)

    confirmed = db.Column(db.Boolean, default=False)

    last_seen = db.Column(db.DateTime(), default=datetime.now)

    ikrss_role_id = db.Column(db.Integer, db.ForeignKey('ikrss_roles.id'))

    ikrss_user_logs = db.relationship(
        'IkrssUserLog', backref='ikrss_user', lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("不能直接get密码")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        # self.ikrss_role_id = role_id
        if self.ikrss_role is None:
            if self.email == current_app.config.get('FLASKY_ADMIN', "iiw.mind@gmail.com"):
                self.ikrss_role = IkrssRole.query.filter_by(permissions=0xff).first()
            if self.ikrss_role is None:
                self.ikrss_role = IkrssRole.query.filter_by(default=True).first()

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<IkrssUser %r, role %r>' % (self.username, self.ikrss_role_id)

    def can(self, permissions):
        return self.ikrss_role is not None and \
               (self.ikrss_role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return IkrssUser.query.get(int(user_id))


class IkrssUserLog(db.Model):
    __tablename__ = "ikrss_users_log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ikrss_user_id = db.Column(db.Integer, db.ForeignKey('ikrss_users.id'))
    date = db.Column(db.Date, default=datetime.now().date(), index=True)
    time = db.Column(db.Time, default=datetime.now().time())
    type = db.Column(db.String(4))

    def __init__(self, type, user):
        self.type = type
        self.ikrss_user_id = user


# ==================================Rss 相关

gikrss_rss_tags = db.Table('ikrss_rsses_tags',
                db.Column('rss_tag_id', db.Integer, db.ForeignKey('ikrss_rss_tags.id')),
                db.Column('rss_resource_id', db.Integer, db.ForeignKey('ikrss_rsses.id'))
                )


class IkrssRssTag(db.Model):
    __tablename__ = "ikrss_rss_tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)

    @staticmethod
    def insert_tags():
        tags=["资讯","博客","学习","娱乐","文学","科技","财经","生活","文化","公众号","知乎"]
        for r in tags:
            tag = IkrssRssTag.query.filter_by(name=r).first()
            if tag is None:
                tmptag = IkrssRssTag(name=r)
                db.session.add(tmptag)
        db.session.commit()


#用户订阅表
gikrss_users_app_rsses = db.Table('ikrss_users_app_rsses',
                db.Column('user_id', db.Integer, db.ForeignKey('ikrss_users.id'),index=True),
                db.Column('rss_resource_id', db.Integer, db.ForeignKey('ikrss_rsses.id'),index=True),

                #推送时间
                db.Column('time', db.Time)
                )


class IkrssRssResource(db.Model):
    __tablename__ = "ikrss_rsses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True)
    desc = db.Column(db.String(255))
    url = db.Column(db.String(4096))

    #订阅数
    subscribe_count = db.Column(db.Integer, default=0)
    # 类型：杂志、书记、rss
    type = db.Column(db.String(10),index=True,default="rss")
    tags = db.relationship('IkrssRssTag', secondary=gikrss_rss_tags,
                           backref=db.backref('rss_resources', lazy='dynamic'))

    users = db.relationship('IkrssUser', secondary=gikrss_users_app_rsses,
                           backref=db.backref('rss_resources', lazy='dynamic'))

    date = db.Column(db.Date, default=datetime.now().date(), index=True)
    time = db.Column(db.Time, default=datetime.now().time())

    def __init__(self, name, desc,url,type,tags):
        self.name=name
        self.desc=desc
        self.url=url
        if type!=None:
            self.type = type
        if tags!=None:
            self.tags=tags

    def __repr__(self):
        '<RssResource %r, id %r>' % (self.name,self.id)



