from typing import List, Dict
import requests


class NewsIngestor:
    """Fetches and processes crypto news articles."""

    def __init__(self, source_url: str):
        self.source_url = source_url

    def fetch_articles(self) -> List[Dict[str, str]]:
        """Fetch raw articles from the source."""
        pass

    def parse_articles(self, raw_data: any) -> List[Dict[str, str]]:
        """Parse and clean raw article data."""
        pass

    def run(self) -> List[Dict[str, str]]:
        """Orchestrates the full ingestion process."""
        pass
