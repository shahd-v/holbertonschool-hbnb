import unittest
from app import create_app

class AdminTestEndpoint(unittest.TestCase):

    def setUp(self):
        """Set up the test client and any necessary test data."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_admins(self):
        """Test retrieving the list of admins."""
        response = self.client.get('/api/v1/admin/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_create_admin(self):
        """Test creating a new admin."""
        new_admin = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }
        response = self.client.post('/api/v1/admin/', json=new_admin)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], new_admin['first_name'])
        self.assertEqual(data['last_name'], new_admin['last_name'])
        self.assertEqual(data['email'], new_admin['email'])

    def test_create_admin_invalid_data(self):
        invalid_admin = {
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email'
        }

        response = self.client.post('/api/v1/admin/', json=invalid_admin)
        self.assertEqual(response.status_code, 400)

