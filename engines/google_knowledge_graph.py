import requests
from engines.engine import Engine


class GoogleKnowledgeGraph(Engine):
    """Google Knowledge Graph description via Serper API.

    Requires SERPER_API_KEY. Returns the short description panel that
    Google shows on the right for entities (people, places, companies).
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
            print(f"[GoogleKnowledgeGraph] {e}")
            return ""
        kg = data.get("knowledgeGraph") or {}
        return kg.get("description", "") or ""


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper. Returns '' if API key is missing."""
    global _instance
    import os
    if not os.getenv("SERPER_API_KEY"):
        return ""
    if _instance is None:
        _instance = GoogleKnowledgeGraph(os.getenv("SERPER_API_KEY"))
    return _instance.search(query, language_code)
