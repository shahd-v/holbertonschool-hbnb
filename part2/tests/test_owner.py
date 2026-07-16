import unittest
from app import create_app

class OwnerTestEndpoint(unittest.TestCase):

    def setUp(self):
        """Set up the test client and any necessary test data."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_owners(self):
        {
        """Test retrieving the list of owners."""
        
        }