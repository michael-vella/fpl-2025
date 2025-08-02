from typing import List

from fpl.api.client import APIClient
from fpl.schemas import TeamResponse

class TeamRepository:
    def __init__(self, client: APIClient = None):
        self._client = client or APIClient()

    def get_all(self) -> List[TeamResponse]:
        json_data = self._client.get_data("bootstrap-static/")
        teams = json_data.get("teams")

        if not teams:
            raise ValueError("No teams found in API response.")
        
        return [TeamResponse(**t) for t in teams]