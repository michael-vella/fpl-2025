from typing import List

from fpl.api.client import APIClient
from fpl.schemas import FixtureResponse

class FixtureRepository:
    def __init__(self, client: APIClient = None):
        self._client = client or APIClient()

    def get_all(self) -> List[FixtureResponse]:
        fixtures = self._client.get_data("fixtures/")

        if not fixtures:
            raise ValueError("No fixtures found in API response.")
        
        return [FixtureResponse(**f) for f in fixtures]