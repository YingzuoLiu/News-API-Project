from typing import List
import asyncio
from .models import NewsProcessor
from .config import Config
from .types import NewsItem, ProcessedNews
from .logger import Logger

class BatchProcessor:
    def __init__(self, config: Config):
        self.config = config
        self.news_processor = NewsProcessor(config)
        self.batch_queue: List[NewsItem] = []
        self.logger = Logger()
        
    async def process_batch(self, items: List[NewsItem]) -> List[ProcessedNews]:
        try:
            self.batch_queue.extend(items)
            
            if len(self.batch_queue) >= self.config.batch_size:
                batch = self.batch_queue[:self.config.batch_size]
                self.batch_queue = self.batch_queue[self.config.batch_size:]
                
                # Process summaries in parallel
                summaries = await asyncio.gather(
                    *[self.news_processor.get_summary(item.text) for item in batch]
                )
                
                # Process sentiments in batch using GPU
                sentiments = [
                    self.news_processor.get_sentiment(item.text) for item in batch
                ]
                
                self.logger.info(f"Successfully processed batch of {len(batch)} items")
                
                return [
                    ProcessedNews(
                        summary=summary,
                        sentiment=sentiment,
                        original_text=item.text
                    )
                    for summary, sentiment, item in zip(summaries, sentiments, batch)
                ]
            return []
        except Exception as e:
            self.logger.error(f"Batch processing error: {str(e)}")
            raise
