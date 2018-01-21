import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG       = False
    TESTING     = False
    CSRF_ENABLED= True
    SECRET_KEY  = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///textmining.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
