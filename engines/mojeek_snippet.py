from base_scraper import BaseScraper
from engines.engine import Engine


class MojeekSnippet(Engine):
    """Mojeek web search via HTML scraping.

    Mojeek is a privacy-focused independent search engine. No API key
    required. Selectors verified against SearXNG's dedicated module:
      https://github.com/searxng/searxng (searx/engines/mojeek.py)
    """

    def __init__(self):
        self.scraper = BaseScraper(headers={
            # SearXNG uses gen_useragent(); we pass a realistic Firefox UA.
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) "
                "Gecko/20100101 Firefox/128.0"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.mojeek.com/",
        })

    def search(self, query: str, language_code: str = "ru") -> str:
        url = "https://www.mojeek.com/search"
        params = {"q": query, "safe": 1}
        html = self.scraper.fetch_html(url, params)
        if not html:
            return ""
        # XPath from SearXNG: content_xpath = '..//p[@class="s"]'
        # CSS equivalent: ul.results-standard li p.s
        return self.scraper.parse_multiple_selectors(
            html,
            [
                "ul.results-standard li p.s",
                "p.s",
                ".s",
            ],
        )


# ---- module-level interface required by the task ----
_instance = None


def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper."""
    global _instance
    if _instance is None:
        _instance = MojeekSnippet()
    return _instance.search(query, language_code)
