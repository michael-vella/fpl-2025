from typing import List

from fpl.api.client import APIClient
from fpl.schemas import GameweekResponse

class GameweekRepository:
    def __init__(self, client: APIClient = None):
        self._client = client or APIClient()

    def get_all(self) -> List[GameweekResponse]:
        json_data = self._client.get_data("bootstrap-static/")
        gameweeks = json_data.get("events")

        if not gameweeks:
            raise ValueError("No gameweeks found in API response.")
        
        return [GameweekResponse(**g) for g in gameweeks]