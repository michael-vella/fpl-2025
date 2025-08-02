import unittest
from datetime import datetime, timezone

from fpl.services import DataParser
from fpl.schemas import (
    PlayerResponse,
    TeamResponse,
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
    
    def test_extract_teams(self):
        sample_json = {
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

        results = DataParser.extract_teams(sample_json)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 1)
        self.assertIsInstance(results[0], TeamResponse)
        self.assertFalse(hasattr(results[0], "extra_args"))

    def test_extract_gameweeks(self):
        deadline_time = datetime(2025, 1, 1, tzinfo=timezone.utc)

        sample_json = {
            "events": [
                {
                    "id": 1,
                    "name": "GW1",
                    "deadline_time": deadline_time,
                    "extra_args": 1,
                }
            ]
        }

        results = DataParser.extract_gameweeks(sample_json)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].deadline_time, deadline_time)
        self.assertIsInstance(results[0], GameWeekResponse)
        self.assertFalse(hasattr(results[0], "extra_args"))

    def test_extract_fixtures(self):
        sample_json = [
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

        results = DataParser.extract_fixtures(sample_json)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 1)
        self.assertIsInstance(results[0], FixtureResponse)
        self.assertFalse(hasattr(results[0], "extra_args"))