# tests/test_auth.py

import unittest
from flask import current_app
from src import create_app, db
from src.models.user import User

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('src.config.TestingConfig')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Create a test user
        self.test_user = User(email='test@example.com', password_hash='hashed_password', is_admin=False)
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_login(self):
        response = self.client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
        data = response.get_json()
        self.assertIn('access_token', data)
        self.assertEqual(response.status_code, 200)

    # Add more test cases as needed

# tests/test_places.py

import unittest
from flask import current_app
from src import create_app, db
from src.models.place import Place
from src.models.user import User

class PlaceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('src.config.TestingConfig')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Create a test user
        self.test_user = User(email='test@example.com', password_hash='hashed_password', is_admin=True)
        db.session.add(self.test_user)
        db.session.commit()

        # Create a test place
        self.test_place = Place(name='Test Place', user_id=self.test_user.id)
        db.session.add(self.test_place)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_update_place_as_admin(self):
        with self.client:
            # Log in as admin
            access_token = self.client.post('/login', json={'email': 'test@example.com', 'password': 'password'}).json['access_token']
            headers = {'Authorization': f'Bearer {access_token}'}

            # Attempt to update place as admin
            response = self.client.put(f'/places/{self.test_place.id}', json={'name': 'Updated Place'}, headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Place updated successfully', response.get_json()['msg'])

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
