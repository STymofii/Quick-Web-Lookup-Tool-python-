import requests
from bs4 import BeautifulSoup
import time
import json
from typing import List


class BaseScraper:
    def __init__(self, delay=0):
        self.delay = delay
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Referer": "https://www.google.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"
        }

    def fetch_html(self, url, params = {}):
        time.sleep(self.delay)
        try:
            session = requests.Session()
            res = session.get(url, params=params, headers=self.headers, timeout=(5, 10))
            # res = requests.get(
            #     url,
            #     impersonate="chrome",
            #     timeout=5,
            #     headers={"Accept-Language": "ru,en;q=0.9"},
            # )
            return res.text if res.status_code == 200 else res.status_code
        except:
            return ""
        
    def fetch_json(self, url, params = {}):
        time.sleep(self.delay)
        try:
            session = requests.Session()
            res = session.get(url, params=params, headers=self.headers, timeout=(5, 10))
            print(res.status_code)
            return res.json() if res.status_code == 200 else {}
        except:
            return {}

    def parse_multiple_selectors(self, html, selectors):
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
