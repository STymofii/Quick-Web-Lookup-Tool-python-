import urllib.parse
import os
from base_scraper import BaseScraper
import requests
import json


def search(query: str, language_code: str = "ru") -> str:
    url = "https://google.serper.dev/search"

    payload = json.dumps({
      "q": query,
      "gl": "uk",
      "hl": language_code
    })
    headers = {
      'X-API-KEY': os.environ.get("SERPER_API_KEY"),
      'Content-Type': 'application/json'
    }

    answer = requests.post(url, headers=headers, data=payload).json()

    return(answer["organic"][0]["snippet"])