import torch
import torch.nn as nn
from transformers import pipeline
import openai
from .config import Config
from .logger import Logger

class NewsProcessor:
    def __init__(self, config: Config):
        self.config = config
        self.logger = Logger()
        self.sentiment_pipeline = pipeline("sentiment-analysis", device=0)
        openai.api_key = config.openai_api_key

    async def get_summary(self, text: str) -> str:
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": "Summarize the following news article:"},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Summarization error: {str(e)}")
            raise

    def get_sentiment(self, text: str) -> float:
        try:
            result = self.sentiment_pipeline(text)[0]
            return float(result['score'])
        except Exception as e:
            self.logger.error(f"Sentiment analysis error: {str(e)}")
            raise