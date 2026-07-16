import unittest 
from app import create_app

class ReviewTestEndpoint(unittest.TestCase):
    def setUp(self):
        """Set up the test client and any necessary test data."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_reviews(self):
        """Test retrieving the list of reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_create_review(self):
        """Test creating a new review."""
        new_review = {
            'user_id': 1,
            'property_id': 1,
            'rating': 5,
            'comment': 'Great place!'
        }
        response = self.client.post('/api/v1/reviews/', json=new_review)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['user_id'], new_review['user_id'])
        self.assertEqual(data['property_id'], new_review['property_id'])
        self.assertEqual(data['rating'], new_review['rating'])
        self.assertEqual(data['comment'], new_review['comment'])

    def test_create_review_invalid_data(self):
        """Test creating a review with invalid data."""
        invalid_review = {
            'user_id': '',
            'property_id': '',
            'rating': 6,  
            'comment': ''
        }
        response = self.client.post('/api/v1/reviews/', json=invalid_review)
        self.assertEqual(response.status_code, 400)