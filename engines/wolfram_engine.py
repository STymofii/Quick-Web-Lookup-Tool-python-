import translators
from base_scraper import BaseScraper
from engines.engine import Engine


class Wolfram_Engine(Engine):
    """Wolfram Alpha short answer. Requires WOLFRAM_TOKEN.

    Free tier: 2000 requests/month. Returns HTTP 501 when Wolfram cannot
    answer — we treat that as empty.
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query: str, language_code: str = "ru") -> str:
        if not self.api_key:
            return ""
        try:
            en_query = query if language_code == "en" else translators.translate_text(
                query, from_language=language_code, to_language="en"
            )
        except Exception:
            en_query = query

        scraper = BaseScraper()
        answer = scraper.fetch_html(
            "https://api.wolframalpha.com/v1/result",
            params={"i": en_query, "appid": self.api_key},
        )
        if not answer:
            return ""
        if language_code == "en":
            return answer
        try:
            return translators.translate_text(
                answer, from_language="en", to_language=language_code
            )
        except Exception:
            return answer


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper. Returns '' if API key is missing."""
    global _instance
    import os
    if not os.getenv("WOLFRAM_TOKEN"):
        return ""
    if _instance is None:
        _instance = Wolfram_Engine(os.getenv("WOLFRAM_TOKEN"))
    return _instance.search(query, language_code)
