from base_scraper import BaseScraper


def search(query: str, language_code: str = "ru") -> str:
    scraper = BaseScraper()
    url = "https://html.duckduckgo.com/html/"
    params = {"q": query, "kl": f"{language_code}-{language_code}"}
    
    html = scraper.fetch_html(url, params)
    
    #selectors = [".result__snippet"]
    selectors = [".d3sXpYMmDKnqC90dk5P7", ".result__snippet"]
    return scraper.parse_multiple_selectors(html, selectors)
