import urllib.parse
import os
from bs4 import BeautifulSoup
from base_scraper import BaseScraper


def search(query: str, language_code: str = "ru") -> str:
    scraper = BaseScraper()
    url = f"https://search.brave.com/search?q={urllib.parse.quote_plus(query)}&source=web"
    
    html = scraper.fetch_html(url)

    selectors = [".infobox-description", ".legend-snippet", ".snippet-description"]
    return scraper.parse_multiple_selectors(html, selectors)