# offer-management/project/tests/base.py

from flask_testing import TestCase

from project.server import db, create_app

from project.config import config
import jwt, hashlib
from datetime import datetime, timedelta

# define basic test case
class BaseTestCase(TestCase):
    #def create_app(self):
        #app.config.from_object(config.TestingConfig)
        #return app
    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

# define auth test case (for testing auth routes)
class AuthTestCase(TestCase):
    #def create_app(self):
        #app.config.from_object(config.TestingConfig)
        #return app
    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        db.drop_all()
        db.create_all()
        db.session.commit()

        salt = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
        salted_password = hashlib.sha256(("test" + salt).encode('utf-8')).hexdigest()

        self.offer_data = {
            "offername": "test",
            "password": salted_password,
            "email": "test@mail.com",
            "salt": salt
        }

    # for mocking purposes
    def create_access_token(self, offer_id):
        payload = {
            'sub': offer_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }
        access_token = jwt.encode(payload, 'secret', algorithm='HS256')
        return access_token

    def tearDown(self):
        db.session.remove()
        db.drop_all()   