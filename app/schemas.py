from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class NewsRequest(BaseModel):
    country: Optional[str] = Field(
        None,
        min_length=2,
        max_length=2,
        description="2-letter country code (e.g. us, fr)"
    )
    category: Optional[str] = Field(
        None,
        description="business, technology, sports, health, science, entertainment"
    )

class Source(BaseModel):
    id: Optional[str]
    name: str

class Article(BaseModel):
    source: Source
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    urlToImage: Optional[str]
    publishedAt: datetime
    content: Optional[str]

class NewsResponse(BaseModel):
    status: str
    totalResults: int
    articles: List[Article]

class ErrorResponse(BaseModel):
    status: str
    code: str
    message: str
