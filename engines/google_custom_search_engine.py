import urllib.parse
import os
from base_scraper import BaseScraper
import requests
import json

def search(query: str, language_code: str = "ru") -> str:
    scraper = BaseScraper()
    url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        "key": os.environ.get("GOOGLE_CUSTOM_SEARCH_API_KEY"),
        "cx": os.environ.get("GOOGLE_CUSTOM_SEARCH_API_ENGINE_ID"),
        "q": query,
        "num": 1,
        "hl": "ru"
    }
    
    try:
        data = scraper.fetch_json(url, params)
        
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0].get("snippet", "")
            
        return ""
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            return "Konchilis zaprosy na sutki"
        return f"API Error: {e}"
    except Exception as e:
        return f"Error: {e}"