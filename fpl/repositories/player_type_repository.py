from typing import List

from fpl.api.client import APIClient
from fpl.schemas import PlayerTypeResponse

class PlayerTypeRepository:
    def __init__(self, client: APIClient = None):
        self._client = client or APIClient()

    def get_all(self) -> List[PlayerTypeResponse]:
        json_data = self._client.get_data("bootstrap-static/")
        player_types = json_data.get("element_types")

        if not player_types:
            raise ValueError("No player types found in API response.")
        
        return [PlayerTypeResponse(**pt) for pt in player_types]