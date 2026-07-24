import urllib.parse
import os
from base_scraper import BaseScraper
import requests
import json


def search(query: str, language_code: str = "ru") -> str:
    scraper = BaseScraper()
    url = "https://www.searchapi.io/api/v1/search"

    params = {
        "engine": "google",
        "q": query,
        "api_key": os.environ.get("SEARCHAPI_API_KEY"),
    }

    
    answer = scraper.fetch_json(url, params)
    #print(json.dumps(answer, indent=2))

    if answer.get("organic_results"):
        return(answer["organic_results"][0]["snippet"])
    return ""

