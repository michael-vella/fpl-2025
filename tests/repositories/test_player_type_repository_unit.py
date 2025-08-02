import unittest
from unittest.mock import MagicMock

from fpl.repositories import PlayerTypeRepository
from fpl.schemas import PlayerTypeResponse


class TestPlayerTypeRepository(unittest.TestCase):
    def test_get_all_returns_player_types(self):
        # Arrange
        mock_client = MagicMock()
        mock_json = {
            "element_types": [
                {
                    "id": 1,
                    "singular_name_short": "DEF",
                    "squad_select": 15,
                    "extra_args": 1,
                }
            ]
        }
        mock_client.get_data.return_value = mock_json
        
        repo = PlayerTypeRepository(mock_client)

        # Act
        player_types = repo.get_all()

        # Assert
        self.assertEqual(len(player_types), 1)
        self.assertEqual(player_types[0].id, 1)
        self.assertIsInstance(player_types[0], PlayerTypeResponse)
        self.assertFalse(hasattr(player_types[0], "extra_args"))
        mock_client.get_data.assert_called_once_with("bootstrap-static/")

    def test_get_all_raises_when_element_types_empty(self):
        # Arrange
        mock_client = MagicMock()
        mock_json = {}
        mock_client.get_data.return_value = mock_json
        
        repo = PlayerTypeRepository(mock_client)

        # Act + Assert
        with self.assertRaises(ValueError):
            repo.get_all()
        
        mock_client.get_data.assert_called_once_with("bootstrap-static/")