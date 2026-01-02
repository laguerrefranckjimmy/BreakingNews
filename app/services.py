import requests
from typing import Optional
from fastapi import HTTPException
from app.config import NEWSAPI_KEY
from app.cache import get_cache, set_cache

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"


def fetch_news(country: Optional[str], category: Optional[str]):
    if not NEWSAPI_KEY:
        raise HTTPException(status_code=500, detail="NewsAPI key not configured")

    cache_key = f"{country or 'all'}:{category or 'all'}"

    # 🔥 Try cache first
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    params = {
        "apiKey": NEWSAPI_KEY,
        "country": country,
        "category": category
    }
    # remove None values
    params = {k: v for k, v in params.items() if v is not None}

    try:
        response = requests.get(NEWSAPI_URL, params=params, timeout=10)
        data = response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=data)

    # 💾 Cache response
    set_cache(cache_key, data)

    return data