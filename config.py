import os
import logging

class Config:
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    LOG_LEVEL = 'INFO'
    CSRF_ENABLED = True
    
    #HTTP SESSION
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT')
    SESSION_TYPE = os.environ.get('SESSION_TYPE')
    
    #postgresql
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #eBird API
    EBIRD_TOKEN = os.environ.get('EBIRD_TOKEN')
    EBIRD_SERVER = os.environ.get('EBIRD_SERVER')
    EBIRD_CONTEXT = os.environ.get('EBIRD_CONTEXT')
    
    #OPENCAGE API
    OPENCAGE_KEY = os.environ.get('OPENCAGE_KEY')
    OPENCAGE_SERVER = os.environ.get('OPENCAGE_SERVER')
    OPENCAGE_CONTEXT = os.environ.get('OPENCAGE_CONTEXT')
    
    #FLASK-CACHING
    CACHE_TYPE = os.environ.get('CACHE_TYPE')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT'))
     
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
