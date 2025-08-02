import unittest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from fpl.repositories import GameweekRepository
from fpl.schemas import GameweekResponse


class TestGameweekRepository(unittest.TestCase):
    def test_get_all_returns_gameweeks(self):
        # Arrange
        mock_client = MagicMock()
        deadline_time = datetime(2025, 1, 1, tzinfo=timezone.utc)
        mock_json = {
            "events": [
                {
                    "id": 1,
                    "name": "GW1",
                    "deadline_time": deadline_time,
                    "extra_args": 1,
                }
            ]
        }
        mock_client.get_data.return_value = mock_json
        
        repo = GameweekRepository(mock_client)

        # Act
        gameweeks = repo.get_all()

        # Assert
        self.assertEqual(len(gameweeks), 1)
        self.assertEqual(gameweeks[0].deadline_time, deadline_time)
        self.assertIsInstance(gameweeks[0], GameweekResponse)
        self.assertFalse(hasattr(gameweeks[0], "extra_args"))
        mock_client.get_data.assert_called_once_with("bootstrap-static/")

    def test_get_all_raises_when_events_empty(self):
        # Arrange
        mock_client = MagicMock()
        mock_json = {}
        mock_client.get_data.return_value = mock_json
        
        repo = GameweekRepository(mock_client)

        # Act + Assert
        with self.assertRaises(ValueError):
            repo.get_all()
        
        mock_client.get_data.assert_called_once_with("bootstrap-static/")