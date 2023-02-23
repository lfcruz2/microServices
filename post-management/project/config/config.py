# user-management/project/config/config.py

import os
from datetime import timedelta

# get base directory
basedir = os.path.join(os.path.dirname(__file__), '..')

# main config class
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = None
    # Auth
    JWT_SECRET_KEY = 'frase-secreta'
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    #PROPAGATE_EXCEPTIONS = False

    @staticmethod
    def init_app(app):
        pass

# development config
class DevelopmentConfig(Config):
    DEBUG = True
    # db auth
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if os.getenv("RUNNING_IN_CONTAINER"):
        # app is running inside a container
        SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    else:
        # app is running locally (DB should be running too otherwise use BlankDB_URL)
        SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")  or \
        'sqlite:///' + os.path.join(basedir, 'server/db/users_dev.sqlite')


# testing config
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'server/db/posts_test.sqlite')
    PRESERVE_CONTEXT_ON_EXCEPTION = False

# production config
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'server/db/posts_prod.sqlite')

# dictionary of config classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
