# user-management/project/tests/test_users.py

import json
import os

# import unittest
from flask import current_app

from project.models import Journey, JourneySchema, AirportSchema
from project.server.journey.views import getJourneyById, getFindByEntrycodeDestinationCodeDate, postNewJourney
from project.tests.base import AuthTestCase

# set environment variables
os.environ['FLASK_ENV'] = 'testing'
os.environ['FLASK_DEBUG'] = '0'

airport_schema = AirportSchema()
journey_schema = JourneySchema()


# test airport endpoints
class TestAirportEndpoints(AuthTestCase):
    """Tests for the Users Service."""

    def test__getAll_airports_endpoint(self):
        response = self.client.get('/routes/airportData')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test__getById_airports_endpoint(self):
        response = self.client.get('/routes/airportById/1')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)
        self.assertTrue('id' in data)
        self.assertTrue('codigo' in data)
        self.assertTrue('aeropuerto' in data)
        self.assertTrue('ciudad' in data)
        self.assertTrue('region_estado' in data)
        self.assertTrue('pais' in data)

    def test__getById_string_airports_endpoint(self):
        response = self.client.get('/routes/airportById/stringParamn')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)
        self.assertTrue('message' in data.keys())
        self.assertTrue('status' in data.keys())
        self.assertTrue(data['status'] == 'fail')

    def test__getById_NotFound_airports_endpoint(self):
        response = self.client.get('/routes/airportById/1001')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(data, dict)
        self.assertGreaterEqual(len(data), 2)
        self.assertTrue('message' in data.keys())
        self.assertTrue('status' in data.keys())
        self.assertTrue(data['status'] == 'fail')

    def test__getByCode_airports_endpoint(self):
        response = self.client.get('/routes/airportByCode/ABC')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)
        self.assertTrue('id' in data)
        self.assertTrue('codigo' in data)
        self.assertTrue('aeropuerto' in data)
        self.assertTrue('ciudad' in data)
        self.assertTrue('region_estado' in data)
        self.assertTrue('pais' in data)

    def test__getByCode_NotFound_airports_endpoint(self):
        response = self.client.get('/routes/airportByCode/1001')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(data, dict)
        self.assertGreaterEqual(len(data), 2)
        self.assertTrue('message' in data.keys())
        self.assertTrue('status' in data.keys())
        self.assertTrue(data['status'] == 'fail')


# set up test database
class TestJourneyService(AuthTestCase):
    """Tests for the Users Service."""

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


# test journey endpoints
class TestJourneyEndpoints(AuthTestCase):
    """Tests endpoints for the Journey Service."""

    def test__get_journeys_endpoint(self):
        response = self.client.get('/routes/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, list)

    def test__getById_journeys_endpoint(self):
        response = getJourneyById(1)
        data = journey_schema.dump(response[0])
        self.assertEqual(response[-1], 200)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, dict)
        self.assertTrue('id' in data)
        self.assertTrue('sourceAirportCode' in data)
        self.assertTrue('destinyAirportCode' in data)
        self.assertTrue('destinyCountry' in data)
        self.assertTrue('bagCost' in data)
        self.assertTrue('createdAt' in data)
        self.assertTrue('expiredAt' in data)

    def test__getById_string_journeys_endpoint(self):
        response = getJourneyById('stringParamn')
        data = response[0]
        self.assertEqual(response[-1], 400)
        self.assertEqual(len(data), 2)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data.keys())
        self.assertTrue('status' in data.keys())
        self.assertTrue(data['status'] == 'fail')

    def test__getById_NotFound_journeys_endpoint(self):
        response = getJourneyById(100)
        data = response[0]
        self.assertEqual(response[-1], 404)
        self.assertEqual(len(data), 2)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data.keys())
        self.assertTrue('status' in data.keys())
        self.assertTrue(data['status'] == 'fail')

    def test__getFindByEntrycodeDestinationCodeDate_ALL_journeys_endpoint(self):
        response = getFindByEntrycodeDestinationCodeDate('AEP', 'AFA', '2023-03-15', '2023-02-13')
        data = journey_schema.dump(response[0][0])
        self.assertEqual(response[-1], 200)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, dict)
        self.assertTrue('id' in data)
        self.assertTrue('sourceAirportCode' in data)
        self.assertTrue('destinyAirportCode' in data)
        self.assertTrue('destinyCountry' in data)
        self.assertTrue('bagCost' in data)
        self.assertTrue('createdAt' in data)
        self.assertTrue('expiredAt' in data)

    def test__getFindByEntrycodeDestinationCodeDate_1_Paramn_journeys_endpoint(self):
        response = getFindByEntrycodeDestinationCodeDate('AEP', None, None, '2023-02-13')
        data = journey_schema.dump(response[0][0])
        self.assertEqual(response[-1], 200)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, dict)
        self.assertTrue('id' in data)
        self.assertTrue('sourceAirportCode' in data)
        self.assertTrue('destinyAirportCode' in data)
        self.assertTrue('destinyCountry' in data)
        self.assertTrue('bagCost' in data)
        self.assertTrue('createdAt' in data)
        self.assertTrue('expiredAt' in data)

    def test__getFindByEntrycodeDestinationCodeDate_2_Paramn_journeys_endpoint(self):
        response = getFindByEntrycodeDestinationCodeDate(None, 'AFA', None, '2023-02-13')
        data = journey_schema.dump(response[0][0])
        self.assertEqual(response[-1], 200)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, dict)
        self.assertTrue('id' in data)
        self.assertTrue('sourceAirportCode' in data)
        self.assertTrue('destinyAirportCode' in data)
        self.assertTrue('destinyCountry' in data)
        self.assertTrue('bagCost' in data)
        self.assertTrue('createdAt' in data)
        self.assertTrue('expiredAt' in data)

    def test__getFindByEntrycodeDestinationCodeDate_3_Paramn_journeys_endpoint(self):
        response = getFindByEntrycodeDestinationCodeDate(None, None, '2023-03-15', '2023-02-13')
        data = journey_schema.dump(response[0][0])
        self.assertEqual(response[-1], 200)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, dict)
        self.assertTrue('id' in data)
        self.assertTrue('sourceAirportCode' in data)
        self.assertTrue('destinyAirportCode' in data)
        self.assertTrue('destinyCountry' in data)
        self.assertTrue('bagCost' in data)
        self.assertTrue('createdAt' in data)
        self.assertTrue('expiredAt' in data)

    def test__getFindByEntrycodeDestinationCodeDate_None_Paramn_journeys_endpoint(self):
        response = getFindByEntrycodeDestinationCodeDate(None, None, None, '2023-02-13')
        data = journey_schema.dump(response[0][0])
        self.assertEqual(response[-1], 200)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, dict)
        self.assertTrue('id' in data)
        self.assertTrue('sourceAirportCode' in data)
        self.assertTrue('destinyAirportCode' in data)
        self.assertTrue('destinyCountry' in data)
        self.assertTrue('bagCost' in data)
        self.assertTrue('createdAt' in data)
        self.assertTrue('expiredAt' in data)

    def test_journeys_ping_endpoint(self):
        response = self.client.get('/routes/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "pong", "status": "success"})


# test user creation
class TestJourneyCreateEndpoint(AuthTestCase):
    """Tests for Users Post Service."""

    def test_create_user(self):
        # given

        new_journey = Journey("FCO", "Italia", "FLW", "Portugal", 20,
                              '2023-02-13 01:11:11.000000',
                              '2023-03-15 01:11:11.000000')

        response = postNewJourney(new_journey)
        data = journey_schema.dump(response[0])
        self.assertEqual(response[-1], 201)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, dict)
        self.assertTrue('id' in data.keys())
        self.assertTrue('createdAt' in data.keys())
        self.assertTrue('expiredAt' in data.keys())
        self.assertIsNotNone(data)
        self.assertEqual(data['createdAt'], "2023-02-13")
        self.assertEqual(data['expiredAt'], "2023-03-15")

        # when

        # response = self.client.post('/routes/', json=new_journey_data, headers={'Authorization': f'Bearer {access_token}'})

        # then
        # self.assertIn('sourceAirportCode', data)
        # self.assertIn('sourceCountry', data)
        # self.assertIn('destinyAirportCode', data)
        # self.assertIn('destinyCountry', data)
        # self.assertIn('bagCost', data)

        # verify the user created is in the database
        # joruney = db.session.query(Journey).filter(Journey.id == 1).first()
        # print(f'User: {user}')
        # self.assertIsNotNone(joruney)
        # self.assertEqual(joruney.sourceAirportCode, "FCO")
        # self.assertEqual(joruney.destinyAirportCode, "FLW")
