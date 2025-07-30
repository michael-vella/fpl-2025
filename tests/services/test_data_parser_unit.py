import unittest

from fpl.services.data_parser import DataParser
from fpl.schemas import (
    PlayerResponse,
    TeamResponse,
    PlayerTypeResponse,
    GameWeekResponse,
    FixtureResponse,
)


class TestDataParser(unittest.TestCase):
    def test_extract_players(self):
        sample_json = {
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
            
            

        results = DataParser.extract_players(sample_json)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].first_name, "Test One")
        self.assertIsInstance(results[0], PlayerResponse)
        self.assertFalse(hasattr(results[0], "extra_args"))