from ddgs import DDGS
from engines.engine import Engine


class DDG_Instant_Answer(Engine):
    """Working 'instant answer' extractor for DuckDuckGo.

    The legacy Instant Answer API (api.duckduckgo.com) is deprecated and
    returns empty JSON for almost every query. Instead we use the `ddgs`
    library to fetch the top result snippet, which is the closest equivalent
    to a short answer from DuckDuckGo.
    """

    def search(self, query: str, language_code: str = "ru") -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    query,
                    region=f"{language_code}-{language_code}",
                    max_results=1,
                ))
                if results:
                    return results[0].get("body", "") or ""
        except Exception as e:
            print(f"[DDG_Instant_Answer] {e}")
        return ""


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper."""
    global _instance
    if _instance is None:
        _instance = DDG_Instant_Answer()
    return _instance.search(query, language_code)
