import os
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    newsapi_key: str = os.getenv("NEWSAPI_KEY")  
    batch_size: int = 2
    max_workers: int = 4
    gpu_ids: List[int] = [0]
    model_name: str = "gpt-3.5-turbo"