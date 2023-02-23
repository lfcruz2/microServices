# post-management/project/tests/test_basics.py

import unittest
from flask import current_app
from project.tests.base import BaseTestCase


class TestBasics(BaseTestCase):
    def test_app_exists(self):
        self.assertFalse(current_app is None)
    
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])