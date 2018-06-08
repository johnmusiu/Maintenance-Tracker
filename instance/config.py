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
    DB_NAME = os.getenv('DB_NAME')


class TestingConfig(Config):
    """ Testing time config """
    TESTING = True
    DEBUG = True
    DB_NAME = os.getenv('DB_TEST')


class StagingConfig(Config):
    """ Staging time config"""
    DEBUG = True
    DB_NAME = os.getenv('DB_NAME')


class ProductionConfig(Config):
    """ Production environment config """
    DEBUG = False
    TESTING = False
    DB_NAME = os.getenv('DB_NAME')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
