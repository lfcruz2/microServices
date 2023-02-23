
# offer-management/project/tests/test_offer.py

import json
from flask import current_app
from sqlalchemy import true
from project.tests.base import AuthTestCase
from app import jwt
from project.models import Offer, db
import os
from datetime import datetime
import json, hashlib
#from project.server.offer.views import create_access_token

# set environment variables
os.environ['FLASK_ENV'] = 'testing'
os.environ['FLASK_DEBUG'] = '0'

# set up test database
class TestOfferService(AuthTestCase):
    """Tests for the Offers Service."""

    def test_app_exists(self):
        self.assertFalse(current_app is None)
            
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

# Check HEALTH Offer service
class TestOfferPingService(AuthTestCase):
    
    def test_offer_ping_endpoint(self):
        response = self.client.get('/offers/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"pong"\n')

# # Check POST offer service
# class TestCreateOfferEndpoint(AuthTestCase):
#     """Tests for Offer Post Service."""

#     def test_create_offer(self):
#         # given
#         new_offer = {
#             "postId": 1,
#             "description": "hello",
#             "size": "SMALL",
#             "fragile": true,
#             "offer": 1,
#             "userId": 1
#         }

#         # when
#         response = self.client.post('/offers/', json=new_offer)
#         data = json.loads(response.data.decode())

#         # then
#         self.assertEqual(response.status_code, 201)
#         self.assertIn('id', data)
#         self.assertIn('userId', data)
#         self.assertIn('createdAt', data)

#         # verify offer was created is in the database
#         offer = db.session.query(Offer).filter(Offer.id==1).first()        
#         self.assertIsNotNone(offer)
#         self.assertEqual(offer.description, "hello")
#         self.assertEqual(offer.size, "SMALL")

# # Check GET offers service
# class TestOfferGetService(AuthTestCase):
    
#     def test_get_offers_endopoint(self):
#         response = self.client.get('/offers/')
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data.decode())
#         self.assertEqual(len(data), 0)
#         self.assertIsInstance(data, list)

# # Check GET offers/<id_offer>
# class TestOfferGetOneService(AuthTestCase):
    
    # def test_get_one_offers_endpoint(self):
    #     # create one offer
    #     new_offer = {
    #         "postId": 1,
    #         "description": "hello",
    #         "size": "SMALL",
    #         "fragile": true,
    #         "offer": 1,
    #         "userId": 1
    #     }        
    #     self.client.post('/offers/', json=new_offer)
        
    #     response = self.client.get('/offers/' + str(1))
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(len(data), 0)
    #     self.assertIsInstance(data, list)