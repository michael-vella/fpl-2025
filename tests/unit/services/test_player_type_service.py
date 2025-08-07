import unittest
from unittest.mock import MagicMock

from fpl.services.player_type_service import PlayerTypeService
from fpl.schemas import PlayerTypeResponse


class TestPlayerTypeService(unittest.TestCase):
    def test_get_id_by_name_found(self):
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [
            PlayerTypeResponse(id=1, singular_name_short="GKP", squad_select=1),
            PlayerTypeResponse(id=2, singular_name_short="DEF", squad_select=2),
        ]

        service = PlayerTypeService(mock_repo)

        # Act + Assert
        self.assertEqual(service.get_id_by_name("GKP"), 1)
        self.assertEqual(service.get_id_by_name("DEF"), 2)

    def test_get_id_by_name_case_insensitive(self):
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [
            PlayerTypeResponse(id=3, singular_name_short="MID", squad_select=3),
        ]

        service = PlayerTypeService(mock_repo)

        # Act + Assert
        self.assertEqual(service.get_id_by_name("mid"), 3)
        self.assertEqual(service.get_id_by_name("mId"), 3)
        self.assertEqual(service.get_id_by_name("MID"), 3)

    def test_get_id_by_name_not_found(self):
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [
            PlayerTypeResponse(id=3, singular_name_short="MID", squad_select=3),
        ]

        service = PlayerTypeService(mock_repo)

        # Act + Assert
        with self.assertRaises(ValueError) as context:
            service.get_id_by_name("fwd")

        self.assertIn("Player type 'fwd' not found", str(context.exception))