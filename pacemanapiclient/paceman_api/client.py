from ..base_client import BaseApiClient
from .models import LiveRuns


class PacemanAPIClient(BaseApiClient):
    BASE_URL: str = "https://paceman.gg/api/ars/"

    def get_liveruns(
        self, version: str = "1.16.1", live_only: bool = False
    ) -> LiveRuns:
        """Returns all live runs"""
        params = {
            "version": version,
            "liveOnly": "true" if live_only else "false",
        }
        return LiveRuns.model_validate(self._make_request("liveruns", params))
