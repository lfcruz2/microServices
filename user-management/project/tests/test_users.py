# user-management/project/tests/test_users.py

import json
#import unittest
from flask import current_app
from project.tests.base import AuthTestCase
from app import jwt
from project.models import User, db
import os
from datetime import datetime
import json, hashlib
from project.server.user.views import create_access_token


# set environment variables
os.environ['FLASK_ENV'] = 'testing'
os.environ['FLASK_DEBUG'] = '0'

# set up test database
class TestUserService(AuthTestCase):
    """Tests for the Users Service."""

    def test_app_exists(self):
        self.assertFalse(current_app is None)
            
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

# test user endpoints
class TestUserEndpoints(AuthTestCase):
    """Tests endpoints for the Users Service."""

    def test__get_users_endpoint(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data), 0)
        self.assertIsInstance(data, list)

    def test_users_ping_endpoint(self):
        response = self.client.get('/users/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "pong", "status": "success"})

# test user creation
class TestUserCreateEndpoint(AuthTestCase):
    """Tests for Users Post Service."""

    def test_create_user(self):
        # given
        new_user_data = {
            "username": "test",
            "password": "test",
            "email": "test@mail.com"
        }

        # when: sending post to create new user
        response = self.client.post('/users/', json=new_user_data)
        data = json.loads(response.data.decode())

        # then: verify the user is created
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)
        self.assertIn('createdAt', data)
        self.assertNotIn('password', data)
        self.assertNotIn('salt', data)
        self.assertNotIn('username', data)

        # verify the user created is in the database
        user = db.session.query(User).filter(User.id==1).first()
        #print(f'User: {user}')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@mail.com")

    def test_create_user_with_missing_fields(self):
        # given: user data with missing fields
        new_user_data = {
            "username": "test",
            "password": "test",
            "email": ""
        }

        # when: sending post to create new user
        response = self.client.post('/users/', json=new_user_data)
        data = json.loads(response.data.decode())

        # then: verify response status 400
        self.assertEqual(response.status_code, 400)
        self.assertIn('fail', data['status'])
        self.assertIn('All fields are required', data['message'])

        # verify the user was not created in the database
        user = db.session.query(User).filter(User.username == "test").first()
        self.assertIsNone(user)


# test user authentication
class TestAuthUser(AuthTestCase):

    def setUp(self):
        super().setUp()
        jwt.init_app(self.app)

    def test_authenticate_user(self):
        # Given a user in the database
        salt = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
        salted_password = hashlib.sha256(("test" + salt).encode('utf-8')).hexdigest()

        user = User(
            username='test',
            email='test@mail.com',
            password=salted_password,
            salt=salt
        )
        db.session.add(user)
        db.session.commit()

        # When the user authenticates with correct credentials
        auth_data = {
            "username": "test",
            "password": "test"
        }
        response = self.client.post('/users/auth/', json=auth_data)
        data = json.loads(response.data)

        # Then the response should contain an access token and an expiration date
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', data)
        self.assertIsInstance(data['token'], str)
        self.assertIn('expireAt', data)
        self.assertIsInstance(data['expireAt'], str)
        expireAt = datetime.fromisoformat(data['expireAt'])
        self.assertLess(datetime.utcnow(), expireAt)

    def test_authenticate_user_with_missing_fields(self):
        # Given a user in the database
        salt = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
        salted_password = hashlib.sha256(("test" + salt).encode('utf-8')).hexdigest()

        user = User(
            username='test',
            email='test@mail.com',
            password=salted_password,
            salt=salt
        )
        db.session.add(user)
        db.session.commit()

        # When the user authenticates with missing fields
        auth_data = {}
        response = self.client.post('/users/auth/', json=auth_data)

        # Then the response should contain an error message and staus 400
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual('fail', data['status'])
        self.assertIn('message', data)
        self.assertEqual('Username and password are required', data['message'])


# test user verification from token
class TestCurrentUser(AuthTestCase):
    """Tests for the CurrentUserResource."""
    def setUp(self):
        super().setUp()
        jwt.init_app(self.app)

        # Disable propagate_exceptions
        #self.app.config['PROPAGATE_EXCEPTIONS'] = False

    def test_get_current_user(self):
        # Given a user in the database
        salt = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
        salted_password = hashlib.sha256(("test" + salt).encode('utf-8')).hexdigest()

        user = User(
            username='test',
            email='test@mail.com',
            password=salted_password,
            salt=salt
        )
        db.session.add(user)
        db.session.commit()

        # When the user authenticates with correct credentials
        auth_data = {
            "username": "test",
            "password": "test"
        }
        response1 = self.client.post('/users/auth/', json=auth_data)
        self.assertEqual(response1.status_code, 200)
        access_token = response1.json['token']

        # check user credentials from access token
        response2 = self.client.get('/users/me/', headers={'Authorization': f'Bearer {access_token}'})

        # Then the response status code should be 200
        self.assertEqual(response2.status_code, 200)

        # Then the response body should contain the expected data
        expected_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        self.assertEqual(response2.json, expected_data)

        # Then the password and salt should not be returned
        self.assertNotIn("password", response2.json)
        self.assertNotIn("salt", response2.json)

        # Attempt to access with invalid token
        response = self.client.get('/users/me/', headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 401)

        # Attempt to access without token
        response = self.client.get('/users/me/')
        self.assertEqual(response.status_code, 400)