# user-management/project/tests/test_config.py

import os
import unittest
from flask import current_app
from flask_testing import TestCase
from project.server import create_app
from app import app
from project.config import config



class TestDevelopmentConfig(TestCase):

    def create_app(self):
        app = create_app('development')
        app.config.from_object(config.DevelopmentConfig)
        return app
    
    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'hard to guess string')
        self.assertFalse(current_app is None)
        #self.assertTrue(
        #    app.config['SQLALCHEMY_DATABASE_URI'] ==
        #    os.environ.get('DEV_DATABASE_URL')
        #)

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object(config.TestingConfig)
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'hard to guess string')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        #self.assertTrue(
        #    app.config['SQLALCHEMY_DATABASE_URI'] ==
        #    os.environ.get('DATABASE_TEST_URL')
        #)

class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object(config.ProductionConfig)
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'hard to guess string')
        #self.assertFalse(app.config['PRODUCTION'])

if __name__ == '__main__':
    unittest.main()