from base_scraper import BaseScraper


def search(query: str, language_code: str = "ru") -> str:
    """Scrape DuckDuckGo HTML endpoint and return the first snippet.

    Works without an API key. Has soft rate limits: after many rapid
    requests DDG returns HTTP 202 and an empty page.
    """
    scraper = BaseScraper()
    url = "https://html.duckduckgo.com/html/"
    params = {"q": query, "kl": f"{language_code}-{language_code}"}
    html = scraper.fetch_html(url, params)
    return scraper.parse_multiple_selectors(html, [".result__snippet", ".result__body"])
