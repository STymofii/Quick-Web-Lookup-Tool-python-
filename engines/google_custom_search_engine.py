from base_scraper import BaseScraper
import json
from engines.engine import Engine

class GoogleCS_Engine(Engine):
    def __init__(self, key, cx):
        """
        Args:
            key (str): os.environ.get(GOOGLE_CUSTOM_SEARCH_API_KEY).
            cx (str, optional): os.environ.get(GOOGLE_CUSTOM_SEARCH_API_ENGINE_ID).
        """
        self.key=key
        self.cx=cx

    def search(self, query: str, language_code: str = "ru") -> str:
        """Search with Google Custom Search Engine.

        does not work, returns an error 403.

        Args:
            query (str): The search phrase or question to query (e.g., "Trump age").
            language_code (str, optional): Two-letter ISO language code for the request.

        Returns:
            str: Extracted snippet text from the top search results, or an empty string
                if no matching selectors or content are found.
        """

        scraper = BaseScraper()
        url = "https://www.googleapis.com/customsearch/v1"
    
        params = {
            "key": self.key,
            "cx": self.cx,
            "q": query,
            "num": 1,
            "hl": "ru"
        }
    
        try:
            data = scraper.fetch_json(url, params)
            print(data)
        
            if "items" in data and len(data["items"]) > 0:
                return data["items"][0].get("snippet", "")
            
            return ""
        
        except Exception as e:
            return f"Error: {e}"