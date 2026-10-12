from base_scraper import BaseScraper
from engines.engine import Engine


class GoogleAnswerBoxHTML(Engine):
    """Google answer box via direct HTML scrape.

    Selector taken from the legacy QA.py implementation:
      div.BNeawe > div > div.BNeawe

    Anti-bot protection usually returns a captcha page. Best-effort.
    """

    def search(self, query: str, language_code: str = "ru") -> str:
        scraper = BaseScraper(headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept-Language": f"{language_code}-{language_code.upper()},{language_code};q=0.9",
        })
        url = "https://www.google.ru/search"
        params = {"q": query, "lr": f"lang_{language_code}", "hl": language_code}
        html = scraper.fetch_html(url, params)
        if not html:
            return ""
        return scraper.parse_multiple_selectors(
            html,
            ["div.BNeawe > div > div.BNeawe", ".hgKElc", ".LGOjhe", ".Z0LcW"],
        )


_instance = None


def search(query: str, language_code: str = "ru") -> str:
    global _instance
    if _instance is None:
        _instance = GoogleAnswerBoxHTML()
    return _instance.search(query, language_code)
