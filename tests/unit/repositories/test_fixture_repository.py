import unittest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from fpl.repositories import FixtureRepository
from fpl.schemas import FixtureResponse


class TestFixtureRepository(unittest.TestCase):
    def test_get_all_returns_fixtures(self):
        # Arrange
        mock_client = MagicMock()
        mock_list = [
            {
                "id": 1,
                "code": 1,
                "event": 1,
                "kickoff_time": datetime(2025, 1, 1, tzinfo=timezone.utc),
                "team_a": 1,
                "team_h": 1,
                "extra_args": 1,
            }
        ]
        mock_client.get_data.return_value = mock_list
        
        repo = FixtureRepository(mock_client)

        # Act
        fixtures = repo.get_all()

        # Assert
        self.assertEqual(len(fixtures), 1)
        self.assertEqual(fixtures[0].id, 1)
        self.assertIsInstance(fixtures[0], FixtureResponse)
        self.assertFalse(hasattr(fixtures[0], "extra_args"))
        mock_client.get_data.assert_called_once_with("fixtures/")

    def test_get_all_raises_when_fixtures_empty(self):
        # Arrange
        mock_client = MagicMock()
        mock_list = []
        mock_client.get_data.return_value = mock_list
        
        repo = FixtureRepository(mock_client)

        # Act + Assert
        with self.assertRaises(ValueError):
            repo.get_all()
        
        mock_client.get_data.assert_called_once_with("fixtures/")