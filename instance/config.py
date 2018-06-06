import os

class Config(object):
    """ base config class """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

class DevelopmentConfig(Config):
    """ Development time config"""
    DEBUG = True
    DB_NAME = 'todos'
    DB_NAME = 'db_live'



class TestingConfig(Config):
    """ Testing time config """
    TESTING = True
    DEBUG = True
    DB_NAME = 'db_test'

class StagingConfig(Config):
    """ Staging time config"""
    DEBUG = True
    DB_NAME = 'db_live'


class ProductionConfig(Config):
    """ Production environment config """
    DEBUG = False
    TESTING = False
    DB_NAME = 'db_live'

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}