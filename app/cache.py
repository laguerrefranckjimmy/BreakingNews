import time
from typing import Any, Dict

# In-memory cache
_cache: Dict[str, Dict[str, Any]] = {}

DEFAULT_TTL = 300  # 5 minutes


def get_cache(key: str):
    entry = _cache.get(key)
    if not entry:
        return None

    if time.time() > entry["expires_at"]:
        del _cache[key]
        return None

    return entry["value"]


def set_cache(key: str, value: Any, ttl: int = DEFAULT_TTL):
    _cache[key] = {
        "value": value,
        "expires_at": time.time() + ttl
    }