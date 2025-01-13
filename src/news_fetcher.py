import aiohttp
import asyncio
from typing import List, Dict, Optional
from .logger import Logger
from .config import Config

class NewsFetcher:
    def __init__(self, config: 'Config'):
        self.config = config
        self.logger = Logger()

    async def fetch_news(self, 
                        country: str = 'us',
                        category: Optional[str] = None,
                        page_size: int = 10) -> List[Dict]:
        """
        从NewsAPI获取新闻
        """
        self.logger.info(f"开始获取新闻 - 国家: {country}, 类别: {category}")
        
        params = {
            'apiKey': self.config.newsapi_key,
            'country': country,
            'pageSize': page_size
        }
        
        if category:
            params['category'] = category

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://newsapi.org/v2/top-headlines',
                    params=params
                ) as response:
                    
                    if response.status != 200:
                        error_msg = f"NewsAPI请求失败: {response.status}"
                        self.logger.error(error_msg)
                        raise Exception(error_msg)
                        
                    data = await response.json()
                    
                    # 转换为我们的格式
                    news_items = []
                    for article in data['articles']:
                        if article['description']:  # 确保有内容
                            news_items.append({
                                "text": article['description'],
                                "source": article['source']['name']
                            })
                    
                    self.logger.info(f"成功获取 {len(news_items)} 条新闻")
                    return news_items
                    
        except Exception as e:
            self.logger.error(f"获取新闻时发生错误: {str(e)}")
            raise