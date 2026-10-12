import requests
from engines.engine import Engine


class WikipediaSummary(Engine):
    """Wikipedia summary via the official REST API.

    Uses https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}
    which returns clean JSON (no HTML, no captcha).

    No API key required.
    """

    def search(self, query: str, language_code: str = "ru") -> str:
        # Wikipedia REST API uses underscores in titles and URL-encoded form
        title = requests.utils.quote(query.strip().replace(" ", "_"))
        url = f"https://{language_code}.wikipedia.org/api/rest_v1/page/summary/{title}"
        try:
            r = requests.get(
                url,
                headers={
                    "User-Agent": "QuickWebLookupTool/1.0 (educational project)",
                    "Accept": "application/json",
                },
                timeout=10,
            )
            if r.status_code != 200:
                return ""
            data = r.json()
            # 'extract' is the short summary, fall back to 'description'
            return (data.get("extract") or data.get("description") or "")[:600]
        except Exception as e:
            print(f"[Wikipedia] {e}")
            return ""


_instance = None


def search(query: str, language_code: str = "ru") -> str:
    global _instance
    if _instance is None:
        _instance = WikipediaSummary()
    return _instance.search(query, language_code)
