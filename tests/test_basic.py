#test
import dotenv
import requests
from dotenv import load_dotenv
import os
load_dotenv()
source_url = os.getenv("API_URL")
Results= requests.get(source_url)
results=Results.json().get("results", [])
print(results)