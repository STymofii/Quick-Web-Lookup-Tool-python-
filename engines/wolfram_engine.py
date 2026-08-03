import os
import translators
from base_scraper import BaseScraper
from engines.engine import Engine

class Wolfram_Engine(Engine):
    def __init__(self, api_key):
        """
        Args:
            api_key (str): os.environ.get(WOLFRAM_TOKEN).
        """
        self.api_key=api_key

    def search(self, query: str, language_code: str = "ru") -> str:
        """Search in Wolfram Alpha.

        Works well, producing acceptable results with limits 2000 requests / month.

        Args:
            query (str): The search phrase or question to query (e.g., "Trump age").
            language_code (str, optional): Two-letter ISO language code for the request.

        Returns:
            str: Extracted snippet text from the top search results, or an empty string
                if no matching selectors or content are found.
        """

        if language_code != "en":
                en_query = translators.translate_text(
                query, from_language=language_code, to_language="en"
            )
        else:
            en_query = query

        url = f"https://api.wolframalpha.com/v1/result"

        params = {
            "input": en_query,
            "appid": self.api_key,
            "output": "json",
            "format": "plaintext" 
        }


        scraper = BaseScraper()
    
        answer = scraper.fetch_html(url, params)
        if language_code != "en":
            return translators.translate_text(
                answer, from_language="en", to_language=language_code
            )

        return answer