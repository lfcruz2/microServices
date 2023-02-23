# post-management/project/server/__init__.py

from flask import Flask
from project.config import config
from project.models import db
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

import os
from project.server.post.views import post_api


# instances
#db = SQLAlchemy()

# app constructor
def create_app(config_name):
    app = Flask(__name__)

    if not config_name:
        config_name = os.getenv('FLASK_ENV', 'development')

    # load .env file
    if config_name == 'development':
        env_file = '.env'
    elif config_name == 'testing':
        env_file = '.env.test'
    elif config_name == 'production':
        env_file = '.env.prod'
    else:
        env_file = '.env'

    load_dotenv(env_file)
    
    # set configuration
    if config_name == 'development':
        app.config.from_object(config.DevelopmentConfig)
    elif config_name == 'testing':
        app.config.from_object(config.TestingConfig)
    elif config_name == 'production':
        app.config.from_object(config.ProductionConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

    # set up database    
    db.init_app(app)

    # register blueprint
    app.register_blueprint(post_api)

    return app
