import unittest
from unittest.mock import MagicMock

from fpl.repositories import TeamRepository
from fpl.schemas import TeamResponse


class TestTeamRepository(unittest.TestCase):
    def test_get_all_returns_teams(self):
        # Arrange
        mock_client = MagicMock()
        mock_json = {
            "teams": [
                {
                    "id": 1,
                    "code": 1,
                    "name": "Team One",
                    "short_name": "One",
                    "strength_overall_home": 1,
                    "strength_overall_away": 1,
                    "strength_attack_home": 1,
                    "strength_attack_away": 1,
                    "strength_defence_home": 1,
                    "strength_defence_away": 1,
                    "extra_args": 1,
                }
            ]
        }
        mock_client.get_data.return_value = mock_json
        
        repo = TeamRepository(mock_client)

        # Act
        teams = repo.get_all()

        # Assert
        self.assertEqual(len(teams), 1)
        self.assertEqual(teams[0].id, 1)
        self.assertIsInstance(teams[0], TeamResponse)
        self.assertFalse(hasattr(teams[0], "extra_args"))
        mock_client.get_data.assert_called_once_with("bootstrap-static/")

    def test_get_all_raises_when_teams_empty(self):
        # Arrange
        mock_client = MagicMock()
        mock_json = {}
        mock_client.get_data.return_value = mock_json
        
        repo = TeamRepository(mock_client)

        # Act + Assert
        with self.assertRaises(ValueError):
            repo.get_all()
        
        mock_client.get_data.assert_called_once_with("bootstrap-static/")