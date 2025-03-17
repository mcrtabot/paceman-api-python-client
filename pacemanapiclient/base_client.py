import typing as t

import requests

from .cache import TimeLimitedCache


class CacheData(t.NamedTuple):
    etag: str
    data: t.Any


cache: TimeLimitedCache[CacheData] = TimeLimitedCache()


class BaseApiClient:
    BASE_URL: str

    def _make_request(
        self,
        endpoint: str,
        params: t.Optional[t.Dict[str, any]] = None,
        use_cache: bool = True,
        cache_ttl: t.Optional[int] = None,
    ) -> any:
        url: str = f"{self.BASE_URL}{endpoint}"
        headers = {}

        cache_key = None
        cached_data = None

        if use_cache:
            cache_key = self._generate_cache_key(endpoint, params)
            cached_data = cache.get(cache_key)
            if cached_data:
                headers["If-None-Match"] = cached_data.etag

        response = requests.get(url, params=params, headers=headers)

        if use_cache:
            if response.status_code == 304:
                if cached_data:
                    cache.touch(cache_key)
                    return cached_data.data
                return cache.get(cache_key).data

        response.raise_for_status()

        response_json = response.json()
        if use_cache:
            if "ETag" in response.headers:
                cache.put(
                    cache_key,
                    CacheData(etag=response.headers["ETag"], data=response_json),
                    ttl=cache_ttl,
                )

        return response_json

    def _generate_cache_key(
        self, endpoint: str, params: t.Optional[t.Dict[str, any]] = None
    ) -> str:
        params = (
            ",".join([f"{k}={v}" for k, v in sorted(params.items())]) if params else ""
        )
        return f"{endpoint}::{params}" if params else endpoint
