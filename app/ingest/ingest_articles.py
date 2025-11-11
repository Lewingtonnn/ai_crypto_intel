from typing import List, Dict
import requests
import asyncio



class NewsIngestor:
    """Fetches and processes crypto news articles."""

    def __init__(self, source_url: str):
        self.source_url = source_url

    def fetch_articles(self) -> List[Dict[str, str]]:
        """Fetch raw articles from the source."""
        try:
            response = requests.get(self.source_url, timeout=10)
            response.raise_for_status()
            return response.json().get("results", [])
        except requests.RequestException as e:
            print(f"Error fetching articles: {e}")
            return []


    def parse_articles(self, raw_data: any) -> List[Dict[str, str]]:
        """Parse and clean raw article data."""
        articles = []
        for item in raw_data:
            article = {
                "id": item.get("id"),
                "slug": str(item.get("slug", "").strip()),
                "title": str(item.get("title", "").strip()),
                "description": item.get("description", ""),
                "published_at": item.get("published_at"),
            }
            articles.append(article)


    def run(self) -> List[Dict[str, str]]:
        """Orchestrates the full ingestion process."""
        pass




#test
import dotenv
from dotenv import load_dotenv
import os
load_dotenv()
source_url = os.getenv("API_URL")
ingestor = NewsIngestor(source_url=source_url)
Results= requests.get(source_url)
results=Results.json().get("results", [])
raw_data=results
articles=[]
for item in raw_data:
    article = {
        "id": item.get("id"),
        "slug": str(item.get("slug", "").strip()),
        "title": str(item.get("title", "").strip()),
        "description": item.get("description"),
        "published_at": item.get("published_at"),
    }
    articles.append(article)

print(articles)