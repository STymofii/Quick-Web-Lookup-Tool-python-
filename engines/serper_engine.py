import requests
import json
from engines.engine import Engine

class Serper_Engine(Engine):
    def __init__(self, api_key):
        """
        Args:
            api_key (str): os.environ.get(SERPER_API_KEY).
        """
        self.api_key=api_key

    def search(self, query: str, language_code: str = "ru") -> str:
        """Search in google with Serper.

        Works well, producing acceptable results with limits 2500 requests

        Args:
            query (str): The search phrase or question to query (e.g., "Trump age").
            language_code (str, optional): Two-letter ISO language code for the request.

        Returns:
            str: Extracted snippet text from the top search results, or an empty string
                if no matching selectors or content are found.
        """

        url = "https://google.serper.dev/search"

        payload = json.dumps({
          "q": query,
          "gl": "uk",
          "hl": language_code
        })
        headers = {
          'X-API-KEY': self.api_key,
          'Content-Type': 'application/json'
        }

        answer = requests.post(url, headers=headers, data=payload).json()
    

        return(answer["organic"][0]["snippet"])