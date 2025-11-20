from typing import List, Dict
import requests
import asyncio
import dotenv
import os
import json
from pathlib import Path
dotenv.load_dotenv()
from app.config_loader import load_config
source_url= os.getenv("API_URL")
if source_url is None:
    raise ValueError("API_URL environment variable is not set.")

from ut1ls.logger import setup_logging
logger = setup_logging()


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

            logger.error(f"Error fetching articles: {e}")

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

    def save_to_json(self, articles, filename="processed_articles.json"):
        """Save parsed articles to JSON in the processed directory."""
        cfg = load_config()
        base_directory= Path(__file__).resolve().parents[2]
        processed_dir = base_directory/cfg.paths["processed_data_dir"]
        processed_dir.mkdir(parents=True, exist_ok=True)


        # Ensure directory exists
        os.makedirs(processed_dir, exist_ok=True)

        filepath = os.path.join(processed_dir, filename)


        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)


        logger.info(f"✅ Saved {len(articles)} articles to {filepath}")


    def run(self) -> List[Dict[str, str]]:
        """Orchestrates the full ingestion process."""

        raw_data = self.fetch_articles()
        if not raw_data:
            return[]
        parsed_articles = self.parse_articles(raw_data)

        parsed_articles = [article for article in parsed_articles if article["content"].strip()]


        self.save_to_json(parsed_articles)

        return parsed_articles

if __name__ == "__main__":
    ingestor = NewsIngestor(source_url)
    articles = ingestor.run()
    for article in articles:

        logger.info(article)
