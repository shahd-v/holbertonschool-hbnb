import unittest 
from app import create_app

class AmenityTestEndpoint(unittest.TestCase):
    def setUp(self):
        """Set up the test client and any necessary test data."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_amenities(self):
        """Test retrieving the list of amenities."""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_create_amenity(self):
        """Test creating a new amenity."""
        new_amenity = {
            'name': 'Free Wi-Fi'
        }
        response = self.client.post('/api/v1/amenities/', json=new_amenity)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], new_amenity['name'])

    def test_create_amenity_invalid_data(self):
        """Test creating an amenity with invalid data."""
        invalid_amenity = {
            'name': ''  
        }
        response = self.client.post('/api/v1/amenities/', json=invalid_amenity)
        self.assertEqual(response.status_code, 400)
