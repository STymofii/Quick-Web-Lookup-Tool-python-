import os
from base_scraper import BaseScraper
import json

from engines.engine import Engine

class SearchAPI_Engine(Engine):
    def __init__(self, api_key):
        """
        Args:
            api_key (str): os.environ.get(SEARCHAPI_API_KEY).
        """
        self.api_key=api_key

    def search(self, query: str, language_code: str = "ru") -> str:
        """Search in google with SearchAPI.

        Works well, producing acceptable results with limits 100 requests/month

        Args:
            query (str): The search phrase or question to query (e.g., "Trump age").
            language_code (str, optional): Two-letter ISO language code for the request.

        Returns:
            str: Extracted snippet text from the top search results, or an empty string
                if no matching selectors or content are found.
        """

        scraper = BaseScraper()
        url = "https://www.searchapi.io/api/v1/search"

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
        }

    
        answer = scraper.fetch_json(url, params)

        if answer.get("organic_results"):
            return(answer["organic_results"][0]["snippet"])
        return ""

