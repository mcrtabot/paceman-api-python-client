import typing as t

import requests


class BaseApiClient:
    BASE_URL: str

    def _make_request(self, endpoint: str, params: t.Optional[t.Dict[str, any]] = None):
        url: str = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
