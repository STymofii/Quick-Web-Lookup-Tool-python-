from base_scraper import BaseScraper
from engines.engine import Engine


class DDG_Snippet(Engine):
    """DEPRECATED. Legacy DuckDuckGo Instant Answer API.

    The endpoint api.duckduckgo.com is no longer maintained and returns
    empty JSON ('Answer': '', 'AbstractText': '') for almost every query.
    Kept for documentation / comparison, not used in benchmarks.
    """

    def search(self, query: str, language_code: str = "ru") -> str:
        scraper = BaseScraper()
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_html": 1}
        data = scraper.fetch_json(url, params)
        if not isinstance(data, dict):
            return ""
        if data.get("Answer"):
            return data["Answer"]
        if data.get("AbstractText"):
            return data["AbstractText"]
        return ""


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper."""
    global _instance
    if _instance is None:
        _instance = DDG_Snippet()
    return _instance.search(query, language_code)
