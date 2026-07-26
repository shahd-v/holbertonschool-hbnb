import unittest
from app import create_app

class OwnerTestEndpoint(unittest.TestCase):

    def setUp(self):
        """Set up the test client and any necessary test data."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_owners(self):
        """Test retrieving the list of owners."""
        response = self.client.get('/api/v1/owners/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_create_owner(self):
        """Test creating a new owner."""
        new_owner = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com'
        }
        response = self.client.post('/api/v1/owners/', json=new_owner)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Alice')
        self.assertEqual(data['last_name'], 'Smith')
        self.assertEqual(data['email'], 'alice.smith@example.com')

    def test_create_owner_invalid_data(self):
        """Test creating an owner with invalid data."""
        invalid_owner = {
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email'
        }
        response = self.client.post('/api/v1/owners/', json=invalid_owner)
        self.assertEqual(response.status_code, 400)
