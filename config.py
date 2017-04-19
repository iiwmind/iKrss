# -*- coding=utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xxxxx key'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    IKRSS_MAIL_SUBJECT_PREFIX = '[IKSS]'
    IKRSS_MAIL_SENDER = 'iKss Admin <iiw.mind@gmail.com>'
    IKRSS_ADMIN = os.environ.get('IKSS_ADMIN') or 'IKSS_ADMIN'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:q@127.0.0.1:3306/ikrss_dev' + "?charset=utf8"
    DEBUG = True

    MIAL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False,

    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "iiw.mind@gmail.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "lmzaizei00"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:q@127.0.0.1:3306/ikrss_test' + "?charset=utf8"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:q@127.0.0.1:3306/ikrss' + "?charset=utf8"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }