# user-management/project/tests/base.py

from datetime import timedelta, datetime
from flask_testing import TestCase
from project.server import db, create_app
#from project.server.post import insertionDB
from app import app
from project.config import config
import jwt, json
import hashlib


class BaseTestCase(TestCase):

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

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        db.drop_all()
        db.create_all()
        db.session.commit()
        #insertionDB.airportInsertionCommands()
        #insertionDB.routeInsertionCommands()

        salt = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
        salted_password = hashlib.sha256(("test" + salt).encode('utf-8')).hexdigest()

        self.user_data = {
                "username": "test",
                "password": salted_password,
                "email": "test@mail.com",
                "salt": salt
        }

    # for mocking purposes
    def create_access_token(self, user_id):
        payload = {
                "jti": "8fb76778-7e3b-40e4-922a-6d296b1186b0",
                "type": "access",
                'sub': user_id,
                'nbf': datetime.utcnow(),
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=30)
        }
        access_token = jwt.encode(payload, 'frase-secreta', algorithm='HS256')
        return access_token

    def tearDown(self):
        db.session.remove()
        db.drop_all()
