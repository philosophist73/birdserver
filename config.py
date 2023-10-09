import os
import logging

class Config:
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    LOG_LEVEL = 'INFO'
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    def get_config():
        config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        }
        flask_env = os.environ.get('FLASK_ENV', 'development').lower()
        return config_map.get(flask_env, DevelopmentConfig)

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
