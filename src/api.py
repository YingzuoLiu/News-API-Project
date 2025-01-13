from fastapi import FastAPI, HTTPException
from typing import List, Optional
from .config import Config
from .batch_processor import BatchProcessor
from .models import NewsProcessor
from .news_fetcher import NewsFetcher
from .logger import Logger
from .types import NewsItem, ProcessedNews

app = FastAPI()
config = Config()
batch_processor = BatchProcessor(config)
news_processor = NewsProcessor(config)
news_fetcher = NewsFetcher(config)
logger = Logger()

@app.post("/process_news/", response_model=List[ProcessedNews])
async def process_news(news_items: List[NewsItem]):
    try:
        logger.info(f"Received processing request: {len(news_items)} news items")
        results = await batch_processor.process_batch(news_items)
        logger.info(f"Successfully processed {len(results)} news items")
        return results
    except Exception as e:
        logger.error(f"Error processing news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fetch_and_process/", response_model=List[ProcessedNews])
async def fetch_and_process(
    country: str = 'us',
    category: Optional[str] = None,
    page_size: int = 10
):
    try:
        logger.info(f"Starting fetch and process - Country: {country}, Category: {category}")
        news_items = await news_fetcher.fetch_news(country, category, page_size)
        results = await batch_processor.process_batch(
            [NewsItem(**item) for item in news_items]
        )
        logger.info(f"Successfully fetched and processed {len(results)} news items")
        return results
    except Exception as e:
        logger.error(f"Error in fetch and process: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
