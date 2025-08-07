import unittest
from unittest.mock import MagicMock

from fpl.repositories import PlayerRepository
from fpl.schemas import PlayerResponse


class TestPlayerRepository(unittest.TestCase):
    def test_get_all_returns_players(self):
        # Arrange
        mock_client = MagicMock()
        mock_json = {
            "elements": [
                {
                    "id": 1,
                    "code": 1,
                    "first_name": "Test One",
                    "second_name": "Test One",
                    "element_type": 1,
                    "now_cost": 1,
                    "team": 1,
                    "expected_goals_per_90": 0.1,
                    "expected_assists_per_90": 0.11,
                    "expected_goal_involvements_per_90": 0.1,
                    "expected_goals_conceded_per_90": 1,
                    "extra_args": 1
                },
                {
                    "id": 2,
                    "code": 2,
                    "first_name": "Test Two",
                    "second_name": "Test Two",
                    "element_type": 2,
                    "now_cost": 2,
                    "team": 2,
                    "expected_goals_per_90": 0.2,
                    "expected_assists_per_90": 0.2,
                    "expected_goal_involvements_per_90": 0.2,
                    "expected_goals_conceded_per_90": 2,
                    "extra_args": 2
                }
            ]
        }
        mock_client.get_data.return_value = mock_json
        
        repo = PlayerRepository(mock_client)

        # Act
        players = repo.get_all()

        # Assert
        self.assertEqual(len(players), 2)
        self.assertEqual(players[0].first_name, "Test One")
        self.assertIsInstance(players[0], PlayerResponse)
        self.assertFalse(hasattr(players[0], "extra_args"))
        mock_client.get_data.assert_called_once_with("bootstrap-static/")

    def test_get_all_raises_when_elements_empty(self):
        # Arrange
        mock_client = MagicMock()
        mock_json = {}
        mock_client.get_data.return_value = mock_json
        
        repo = PlayerRepository(mock_client)

        # Act + Assert
        with self.assertRaises(ValueError):
            repo.get_all()
        
        mock_client.get_data.assert_called_once_with("bootstrap-static/")