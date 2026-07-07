from base_scraper import BaseScraper


def search(query: str, language_code: str = "ru") -> str:
    scraper = BaseScraper()
    url = "https://www.google.com/search"
    params = {"q": query, "hl": language_code}
    
    html = scraper.fetch_html(url, params)

    selectors = [".hgKElc", ".LGOjhe", ".Z0LcW"]
    return scraper.parse_multiple_selectors(html, selectors)
