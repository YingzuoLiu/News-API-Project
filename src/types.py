from pydantic import BaseModel
from typing import List, Optional

class NewsItem(BaseModel):
    text: str
    source: str

class ProcessedNews(BaseModel):
    summary: str
    sentiment: float
    original_text: str