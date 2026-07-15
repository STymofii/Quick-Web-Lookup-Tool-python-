import urllib.parse
from base_scraper import BaseScraper
import json


def search(query: str, language_code: str = "ru") -> str:
    scraper = BaseScraper()
    url = f"https://api.duckduckgo.com/?q={urllib.parse.quote_plus(query)}&format=json&no_html=1"
    
    answer = scraper.fetch_json(url)
    if answer.get("Answer"):
       return(answer["Answer"])
    elif answer.get("AbstractText"):
        return(answer["AbstractText"])

    return answer
