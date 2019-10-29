import os

class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SECRET_KEY = 'xcjytebjby6fdsohsdcpdasksksa8237qcyycefgjydtvhb'
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd().replace('\\','/') + '/userDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = True