import requests
import json

# Your Deployment URL
API_URL = "https://crypto-rag-api-351995124578.us-central1.run.app/api/v1/query"


def ask_the_oracle(question):
    payload = {"query": question}
    headers = {"Content-Type": "application/json"}

    print(f"📡 Sending query to Cloud Run: '{question}'...")

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()

        print("\n📝 --- INTELLIGENCE REPORT ---")
        print(data["answer"])
        print("\n🔍 --- SOURCES ---")
        for source in data["sources"]:
            print(f"- {source['slug']} (Score: {source['similarity_score']:.2f})")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    ask_the_oracle("What is the latest news regarding Ethereum and gas fees?")