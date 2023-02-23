# post-management/project/tests/test_post.py

from datetime import timedelta, datetime
import json
from urllib.parse import urlparse
from random import randint
import unittest

from project.server.post.views import createPost
from flask import current_app
from project.tests.base import BaseTestCase
from project.server import db
from project.models import Post
from project.server.post.views import create_access_token
import jwt, json
import os


os.environ['FLASK_ENV'] = 'testing'
os.environ['FLASK_DEBUG'] = '0'

class TestPostService(BaseTestCase):
    """Tests for the Posts Service."""

    def test_posts(self):
        print("STEP: TESTING POSTS/SING")
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/posts/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_app_exists(self):
        self.assertFalse(current_app is None)
        
    
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

class TestPostEndpoints(BaseTestCase):
    """Tests endpoints for the Posts Service."""


class TestPostCreateEndpoint(BaseTestCase):
    """Tests for Posts Post Service"""

    def test_create_post(self):
        userId = randint(0,100)
        routeId = randint(0,100)
        plannedStartDate = "2023-02-14"
        plannedEndDate = "2023-02-24"
        startDate = datetime.strptime(plannedStartDate,'%Y-%m-%d')
        endDate = datetime.strptime(plannedEndDate,'%Y-%m-%d')
        response = createPost(userId, routeId, startDate, endDate)
        postFounded = Post.query.filter_by(id=response['id']).first()
        assert postFounded.userId == userId
        assert postFounded.routeId == routeId

    def test_create_post_without_route_id(self):
        userId = randint(0,100)
        plannedStartDate = "2023-02-14"
        plannedEndDate = "2023-02-24"
        startDate = datetime.strptime(plannedStartDate,'%Y-%m-%d')
        endDate = datetime.strptime(plannedEndDate,'%Y-%m-%d')
        response = createPost(userId, None, startDate, endDate)
        assert response['error'] == True

    def test_create_post_without_user_id(self):
        routeId = randint(0,100)
        plannedStartDate = "2023-02-14"
        plannedEndDate = "2023-02-24"
        startDate = datetime.strptime(plannedStartDate,'%Y-%m-%d')
        endDate = datetime.strptime(plannedEndDate,'%Y-%m-%d')
        response = createPost(None, routeId, startDate, endDate)
        assert response['error'] == True 

    def test_create_post_without_start_date(self):
        userId = randint(0,100)
        routeId = randint(0,100)
        plannedEndDate = "2023-02-24"
        endDate = datetime.strptime(plannedEndDate,'%Y-%m-%d')
        response = createPost(userId, routeId, None, endDate)
        assert response['error'] == True 

    def test_create_post_without_end_date(self):
        userId = randint(0,100)
        routeId = randint(0,100)
        plannedStartDate = "2023-02-14"
        startDate = datetime.strptime(plannedStartDate,'%Y-%m-%d')
        response = createPost(userId, routeId, startDate, None)
        assert response['error'] == True         


"""
class TestCurrentPostResource(AuthTestCase):
    Tests for the Current Post Resource.

    def test_get_current_user(self):
        response = self.client.get('/posts/me')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email
        })

    def test_auth_endpoint(self):
        # request body data
        data = {
            'username': 'test',
            'password': 'test'
        }
        headers = {'Content-Type': 'application/json'}

        # response
        response = self.client.post('/posts/auth', data=json.dumps(data), headers=headers)

        # Assert
        self.assertEqual(response.status_code, 200)
        # Verification of the response
        self.assertIn('id', response.json)
        self.assertIn('token', response.json)
        self.assertIn('expireAt', response.json)

"""
""" if __name__ == '__main__':
    unittest.main() """