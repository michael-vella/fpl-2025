from fpl.schemas import (
    PlayerResponse,
    TeamResponse,
    GameWeekResponse,
    FixtureResponse,
)


class DataParser:
    @staticmethod
    def _extract(json_data: dict, key: str, model) -> list:
        return [model(**item) for item in json_data.get(key, [])]

    extract_players = staticmethod(lambda d: DataParser._extract(d, "elements", PlayerResponse))
    extract_teams = staticmethod(lambda d: DataParser._extract(d, "teams", TeamResponse))
    extract_gameweeks = staticmethod(lambda d: DataParser._extract(d, "events", GameWeekResponse))
    extract_fixtures = staticmethod(lambda d: [FixtureResponse(**f) for f in d])  # list, not dict