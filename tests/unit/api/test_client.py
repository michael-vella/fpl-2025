import unittest
from unittest.mock import patch, MagicMock

from fpl.api.client import APIClient, APIClientError


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mock_url: str = "mock-endpoint/"
    
    def test_get_data_success(self):
        fake_response = {"players": []}

        url: str = self.client.base_url + self.mock_url

        with patch.object(self.client.session, "get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = fake_response
            
            mock_get.return_value = mock_response

            data = self.client.get_data(relative_url=self.mock_url)
            self.assertEqual(data, fake_response)
            mock_get.assert_called_once_with(url)
    
    def test_get_data_failure(self):
        with patch.object(self.client.session, "get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"

            mock_get.return_value = mock_response

            with self.assertRaises(APIClientError) as context:
                self.client.get_data(relative_url=self.mock_url)
            
            self.assertIn("GET failed", str(context.exception))
