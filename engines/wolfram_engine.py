import os
import requests
import translators
from base_scraper import BaseScraper


def search(query: str, language_code: str = "ru") -> str:
    """Search in Wolfram Alpha.

    Works well, producing acceptable results with limits 2000 requests / month.

    Args:
        query (str): The search phrase or question to query (e.g., "Trump age").
        language_code (str, optional): Two-letter ISO language code for the request.

    Returns:
        str: Extracted snippet text from the top search results, or an empty string
            if no matching selectors or content are found.
    """

    if not os.environ.get("WOLFRAM_TOKEN"):
        return "Error: not found WOLFRAM_TOKEN in .env"

    if language_code != "en":
            en_query = translators.translate_text(
            query, from_language=language_code, to_language="en"
        )
    else:
        en_query = query

    url = f"https://api.wolframalpha.com/v1/result"

    params = {
        "input": en_query,
        "appid": os.environ.get("WOLFRAM_TOKEN"),
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