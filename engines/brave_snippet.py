import urllib.parse
import os
from bs4 import BeautifulSoup
from base_scraper import BaseScraper


def search(query: str, language_code: str = "ru") -> str:
    """Search in Brave.

    !!!DOESN'T WORK DUE TO ANTIBOT CHECK!!!

    Args:
        query (str): The search phrase or question to query (e.g., "Trump age").
        language_code (str, optional): Two-letter ISO language code for the request.

    Returns:
        str: Extracted snippet text from the top search results, or an empty string
            if no matching selectors or content are found.
    """

    scraper = BaseScraper()
    url = f"https://search.brave.com/search?q={urllib.parse.quote_plus(query)}&source=web"
    
    html = scraper.fetch_html(url)

    selectors = [".infobox-description", ".legend-snippet", ".snippet-description"]
    return scraper.parse_multiple_selectors(html, selectors)