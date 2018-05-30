import os

class Config(object):
    """ base config class """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

class DevelopmentConfig(Config):
    """ Development time config"""
    DEBUG = True

class TestingConfig(Config):
    """ Testing time config """
    TESTING = True
    DEBUG = True

class StagingConfig(Config):
    """ Staging time config"""
    DEBUG = True

class ProductionConfig(Config):
    """ Production environment config """
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}