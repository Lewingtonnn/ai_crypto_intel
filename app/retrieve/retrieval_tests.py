
from app.retrieve.query_engine import QueryEngine

if __name__ == "__main__":
    qe = QueryEngine()
    query = "Bitcoin ETFs"
    results = qe.retrieve_similar(query, n_results=3)


    for r in results:
        print(f"\n📰 {r['slug']} | {r['similarity_score']:.4f}")
        print(f"Published at: {r['published_at']}")
        print(f"Snippet: {r['content'][:200]}...")
