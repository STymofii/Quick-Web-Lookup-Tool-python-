from base_scraper import BaseScraper
from engines.engine import Engine

class GoogleSnippet(Engine):
    def search(self, query: str, language_code: str = "ru") -> str:
        """Search in Google.

        It doesn't work, it's extremely difficult to find the right selectors, and it often returns an anti-bot stub.

        Args:
            query (str): The search phrase or question to query (e.g., "Trump age").
            language_code (str, optional): Two-letter ISO language code for the request.

        Returns:
            str: Extracted snippet text from the top search results, or an empty string
                if no matching selectors or content are found.
        """

        scraper = BaseScraper()
        url = "https://www.google.com/search"
        params = {"q": query, "hl": language_code}
    
        html = scraper.fetch_html(url, params)

        selectors = [".hgKElc", ".LGOjhe", ".Z0LcW"]
        return scraper.parse_multiple_selectors(html, selectors)


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper."""
    global _instance
    if _instance is None:
        _instance = GoogleSnippet()
    return _instance.search(query, language_code)
