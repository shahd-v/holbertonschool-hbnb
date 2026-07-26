import unittest
from app import create_app

class usersTestEndpoint(unittest.TestCase):

    def setUp(self):
        """Set up the test client and any necessary test data."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_users(self):
        """Test retrieving the list of users."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_create_user(self):
        """Test creating a new user."""
        new_user = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com'
        }
        response = self.client.post('/api/v1/users/', json=new_user)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], new_user['first_name'])
        self.assertEqual(data['last_name'], new_user['last_name'])
        self.assertEqual(data['email'], new_user['email'])

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data."""
        invalid_user = {
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email'
        }
        response = self.client.post('/api/v1/users/', json=invalid_user)
        self.assertEqual(response.status_code, 400)