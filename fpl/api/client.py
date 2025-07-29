import requests


class APIClientError(Exception):
    pass


class APIClient:
    def __init__(self) -> None:
        self.base_url: str = "https://fantasy.premierleague.com/api/"
        self.session = requests.Session()

    def get_data(self, relative_url: str) -> dict:
        url: str = self.base_url + relative_url
        response: requests.Response = self.session.get(url)
        if response.status_code != 200:
            raise APIClientError(f"GET failed: {response.text}")
        return response.json()