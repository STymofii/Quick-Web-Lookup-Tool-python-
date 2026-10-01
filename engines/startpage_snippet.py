from base_scraper import BaseScraper
from engines.engine import Engine


class StartpageSnippet(Engine):
    """Startpage web search via HTML scraping.

    Startpage is a Google proxy with strong anti-bot protection. Direct
    scraping often returns captcha or empty pages. This implementation
    makes a best-effort attempt with realistic headers.

    Evidence: multiple search-engine-scraper projects (SearXNG, etc.)
    report Startpage as unreliable for programmatic access.
    """

    def __init__(self):
        self.scraper = BaseScraper(headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://www.startpage.com/",
        })

    def search(self, query: str, language_code: str = "ru") -> str:
        url = "https://www.startpage.com/sp/search"
        params = {"query": query, "cat": "web"}
        html = self.scraper.fetch_html(url, params)
        if not html:
            return ""
        # Startpage results use .result and .description classes
        return self.scraper.parse_multiple_selectors(
            html,
            [
                "div#results div.result p.description",
                "div.result p",
                ".w-gl__description",
                ".description",
            ],
        )


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper."""
    global _instance
    if _instance is None:
        _instance = StartpageSnippet()
    return _instance.search(query, language_code)
