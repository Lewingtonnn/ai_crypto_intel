from typing import List, Dict
import requests
import asyncio
import dotenv
import os
dotenv.load_dotenv()
source_url= os.getenv("API_URL")
if source_url is None:
    raise ValueError("API_URL environment variable is not set.")



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
            title = str(item.get("title", "").strip())
            description = item.get("description")
            content = title
            if description:
                content += description
            article = {
                "id": item.get("id"),
                "slug": str(item.get("slug", "").strip()),
                "title": title,
                "description": description,
                "content": content,
                "published_at": item.get("published_at"),
            }
            articles.append(article)
        return articles



    def run(self) -> List[Dict[str, str]]:
        """Orchestrates the full ingestion process."""
        raw_data = self.fetch_articles()
        if not raw_data:
            return[]
        parsed_articles = self.parse_articles(raw_data)

        parsed_articles = [article for article in parsed_articles if article["content"].strip()]

        return parsed_articles

if __name__ == "__main__":
    ingestor = NewsIngestor(source_url)
    articles = ingestor.run()
    for article in articles:
        print(article)
