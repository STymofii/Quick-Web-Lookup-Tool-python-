import requests
from engines.engine import Engine


class QwantSnippet(Engine):
    """Qwant web search via the (undocumented) v3 API.

    No API key required, but the API is rate-limited (HTTP 429 after
    bursts) and requires a valid 'tgp' parameter and correct headers,
    otherwise returns an empty JSON body.

    Reverse-engineered from Qwant's own network traffic and SearXNG:
      https://github.com/searxng/searxng/blob/master/searx/engines/qwant.py
    """

    def search(self, query: str, language_code: str = "ru") -> str:
        url = "https://api.qwant.com/v3/search/web"
        params = {
            "q": query,
            "count": 1,
            "locale": f"{language_code}_{language_code.upper()}",
            "offset": 0,
            "device": "desktop",
            "tgp": 1,
            "safesearch": 1,
            "displayed": "true",
        }
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json",
            "Referer": "https://www.qwant.com/",
            "Origin": "https://www.qwant.com",
        }
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=15)
            if resp.status_code != 200:
                return ""
            data = resp.json()
        except Exception as e:
            print(f"[Qwant] {e}")
            return ""

        if data.get("status") != "success":
            return ""

        mainline = (
            data.get("data", {})
            .get("result", {})
            .get("items", {})
            .get("mainline", [])
        )
        for block in mainline:
            if block.get("type") != "web":
                continue
            for item in block.get("items", []):
                desc = item.get("desc", "")
                if desc:
                    return desc
        return ""


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper."""
    global _instance
    if _instance is None:
        _instance = QwantSnippet()
    return _instance.search(query, language_code)
