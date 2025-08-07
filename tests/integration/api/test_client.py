import unittest

from fpl.api.client import APIClient, APIClientError


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_data_success(self):
        data = self.client.get_data(relative_url="bootstrap-static/")
        self.assertIsInstance(data, dict)
        self.assertTrue("elements" in data)
    
    def test_get_data_failure(self):
        with self.assertRaises(APIClientError):
            self.client.get_data("fake-endpoint")