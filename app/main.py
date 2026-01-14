from typing import Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.schemas import NewsResponse
from app.services import fetch_news

app = FastAPI(
    title="Serverless News API",
    description="Fetch news by country or category",
    version="1.3.0"
)

# ===========================
# ✅ PRODUCTION-GRADE CORS
# ===========================
# Allow:
#  - localhost with any port for dev
#  - root and www domain
allow_origin_regex = r"^https?://(localhost:\d+|francklab\.fyi|www\.francklab\.fyi)$"

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # OPTIONS included for preflight
    allow_headers=["*"],
)

# Prefix for API Gateway
PREFIX = "/news-api"

# === Health endpoint ===
@app.get(f"{PREFIX}/health")
def health():
    return {"status": "ok"}

# === Get news endpoint ===
@app.get(f"{PREFIX}/news", response_model=NewsResponse)
def get_news(
    country: Optional[str] = Query(None, min_length=2, max_length=2),
    category: Optional[str] = Query(None)
):
    return fetch_news(country, category)

# ===========================
# AWS Lambda handler
# ===========================
handler = Mangum(app)
