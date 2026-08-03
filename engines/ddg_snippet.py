import urllib.parse
from base_scraper import BaseScraper
import json
from engines.engine import Engine

class DDG_Snippet(Engine):
    def search(self, query: str, language_code: str = "ru") -> str:
        """Search with DuckDuckGo API.

        It doesn't work and returns json without values.

        Args:
            query (str): The search phrase or question to query (e.g., "Trump age").
            language_code (str, optional): Two-letter ISO language code for the request.

        Returns:
            str: Extracted snippet text from the top search results, or an empty string
                if no matching selectors or content are found.
        """

        scraper = BaseScraper()
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote_plus(query)}&format=json&no_html=1"
    
        answer = scraper.fetch_json(url)
        if answer.get("Answer"):
           return(answer["Answer"])
        elif answer.get("AbstractText"):
            return(answer["AbstractText"])

        return answer
