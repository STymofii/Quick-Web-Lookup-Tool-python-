import requests
from engines.engine import Engine


class GoogleCalculator(Engine):
    """Google calculator result via Serper API. Requires SERPER_API_KEY.

    Works for pure math queries like '2+2*2', '15% of 200'.
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query: str, language_code: str = "ru") -> str:
        if not self.api_key:
            return ""
        try:
            resp = requests.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": self.api_key,
                    "Content-Type": "application/json",
                },
                json={"q": query, "gl": "uk", "hl": language_code},
                timeout=15,
            )
            data = resp.json()
        except Exception as e:
            print(f"[GoogleCalculator] {e}")
            return ""
        calc = data.get("calculator") or {}
        return calc.get("result", "") or ""


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper. Returns '' if API key is missing."""
    global _instance
    import os
    if not os.getenv("SERPER_API_KEY"):
        return ""
    if _instance is None:
        _instance = GoogleCalculator(os.getenv("SERPER_API_KEY"))
    return _instance.search(query, language_code)
