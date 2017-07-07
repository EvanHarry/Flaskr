import json
import unittest

from app import create_app, db
from app.models import User


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        u = User(username='test', password='test')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_token_auth(self):
        response = self.client.post(
            '/token', content_type='application/json',
            data=json.dumps({'username': 'test', 'password': 'test'})
        )
        self.assertTrue(response.status_code == 200)

        response = self.client.post(
            '/token', content_type='application/json',
            data=json.dumps({'username': 'test', 'password': 'incorrect_test'})
        )
        self.assertTrue(response.status_code == 401)

        response = self.client.post(
            '/token',
            data=json.dumps({'username': 'test', 'password': 'test'})
        )
        self.assertTrue(response.status_code == 400)

        response = self.client.post(
            '/token', content_type='application/json',
            data=json.dumps({'incorrect_field': 'test', 'password': 'test'})
        )
        self.assertTrue(response.status_code == 400)

        response = self.client.post(
            '/token', content_type='application/json',
            data=json.dumps({'username': 'test', 'incorrect_field': 'test'})
        )
        self.assertTrue(response.status_code == 400)

        response = self.client.post(
            '/token', content_type='application/json',
            data=json.dumps({'username': 'incorrect_test', 'password': 'test'})
        )
        self.assertTrue(response.status_code == 404)
