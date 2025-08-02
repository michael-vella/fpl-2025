from typing import List

from fpl.api.client import APIClient
from fpl.schemas import PlayerResponse

class PlayerRepository:
    def __init__(self, client: APIClient = None):
        self._client = client or APIClient()

    def get_all(self) -> List[PlayerResponse]:
        json_data = self._client.get_data("bootstrap-static/")
        players = json_data.get("elements")

        if not players:
            raise ValueError("No players found in API response.")
        
        return [PlayerResponse(**p) for p in players]