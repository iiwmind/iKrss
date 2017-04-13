# -*- coding=utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xxxxx key'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    IKSS_MAIL_SUBJECT_PREFIX = '[IKSS]'
    IKSS_MAIL_SENDER = 'iKss Admin <iiw.mind@gmail.com>'
    IKSS_ADMIN = os.environ.get('IKSS_ADMIN') or 'IKSS_ADMIN'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:q@127.0.0.1:3306/iKssDbDev' + "?charset=utf8"
    DEBUG = True

    MIAL_SERVER = 'smtp.googleemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "iiw.mind@gmail.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "lmzaizei00"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:q@127.0.0.1:3306/iKssDbTest' + "?charset=utf8"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:q@127.0.0.1:3306/iKssDb' + "?charset=utf8"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }