from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

def split_article_content(articles: List[Dict]) -> List[Dict]:
    """
    Splits the 'content' of each article into smaller chunks,
    maintaining original metadata for each chunk.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )

    chunked_articles = []
    for article in articles:
        text_chunks = text_splitter.split_text(article["content"])

        # Create a new document entry for each chunk
        for i, chunk in enumerate(text_chunks):
            chunk_id = f"{article['id']}-{i}"

            chunked_articles.append({
                "id": chunk_id,
                "content": chunk,
                # Inherit all original metadata
                "slug": article["slug"],
                "published_at": article["published_at"],
                "original_id": article["id"], # Keep a reference to the parent
            })

    return chunked_articles