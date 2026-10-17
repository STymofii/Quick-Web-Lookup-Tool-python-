import time
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup


class BaseScraper:
    """HTTP + HTML/JSON parsing helper shared by all scraper engines."""

    def __init__(self, delay: float = 0, headers: Dict[str, str] | None = None):
        self.delay = delay
        self.headers = headers or {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8"
            ),
        }

    def fetch_html(self, url: str, params: Dict[str, Any] | None = None) -> str:
        if self.delay:
            time.sleep(self.delay)
        try:
            res = requests.get(url, params=params or {}, headers=self.headers, timeout=(5, 15))
            return res.text if res.status_code == 200 else ""
        except requests.RequestException:
            return ""

    def fetch_json(self, url: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        if self.delay:
            time.sleep(self.delay)
        try:
            res = requests.get(url, params=params or {}, headers=self.headers, timeout=(5, 15))
            if res.status_code != 200:
                return {}
            return res.json()
        except (requests.RequestException, ValueError):
            return {}

    def parse_selector(self, html: str, selector: str) -> str:
        """Return text of the first matching CSS selector, or empty string."""
        if not html:
            return ""
        soup = BeautifulSoup(html, "html.parser")
        target = soup.select_one(selector)
        if not target:
            return ""
        return target.get_text(separator=" ", strip=True)

    def parse_multiple_selectors(self, html: str, selectors: List[str]) -> str:
        """Try each selector in order, return the first non-empty text."""
        if not html:
            return ""
        soup = BeautifulSoup(html, "html.parser")
        for selector in selectors:
            target = soup.select_one(selector)
            if target:
                text = target.get_text(separator=" ", strip=True)
                if text:
                    return text
        return ""
