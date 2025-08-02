import unittest

from fpl.services.player_type_service import PlayerTypeService
from fpl.schemas import PlayerTypeResponse


class TestPlayerTypeService(unittest.TestCase):
    def test_get_id_by_name_found(self):
        player_types = [
            PlayerTypeResponse(id=1, singular_name="Goalkeeper", singular_name_short="GKP", squad_select=1),
            PlayerTypeResponse(id=2, singular_name="Defender", singular_name_short="DEF", squad_select=2),
        ]
        service = PlayerTypeService(player_types)

        self.assertEqual(service.get_id_by_name("Goalkeeper"), 1)
        self.assertEqual(service.get_id_by_name("Defender"), 2)

    def test_get_id_by_name_case_insensitive(self):
        player_types = [
            PlayerTypeResponse(id=3, singular_name="Midfielder", singular_name_short="MID", squad_select=3),
        ]
        service = PlayerTypeService(player_types)

        self.assertEqual(service.get_id_by_name("midfielder"), 3)
        self.assertEqual(service.get_id_by_name("MIDFIELDER"), 3)

    def test_get_id_by_name_not_found(self):
        player_types = []
        service = PlayerTypeService(player_types)

        with self.assertRaises(ValueError) as context:
            service.get_id_by_name("Striker")

        self.assertIn("Player type 'Striker' not found", str(context.exception))