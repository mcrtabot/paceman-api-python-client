import time
from threading import Lock
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class TimeLimitedCache(Generic[T]):
    def __init__(self, default_ttl: Optional[int] = None):
        self.cache = {}
        self.default_ttl = default_ttl
        self.lock = Lock()

    def _is_expired(self, entry_time: float, ttl: int) -> bool:
        return time.time() - entry_time > ttl

    def _cleanup(self):
        with self.lock:
            keys_to_remove = [
                k for k, (v, t, tl) in self.cache.items() if self._is_expired(t, tl)
            ]
            for k in keys_to_remove:
                del self.cache[k]

    def get(self, key) -> Optional[T]:
        self._cleanup()
        with self.lock:
            item = self.cache.get(key, None)
            return item[0] if item else None

    def put(self, key, value: T, ttl: Optional[int] = None):
        self._cleanup()
        with self.lock:
            effective_ttl = ttl if ttl is not None else self.default_ttl
            if effective_ttl is None:
                raise ValueError("ttl is required")
            self.cache[key] = (value, time.time(), effective_ttl)

    def touch(self, key):
        with self.lock:
            if key in self.cache:
                self.cache[key] = (self.cache[key][0], time.time(), self.cache[key][2])
