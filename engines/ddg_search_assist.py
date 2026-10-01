from ddgs import DDGS
from engines.engine import Engine


class DDG_Search_Assist(Engine):
    """DuckDuckGo Search Assist.

    DDG's 'Search Assist' feature provides an AI-generated summary.
    There is no public API for it, but we can approximate it by fetching
    several DDGS text results and concatenating their bodies — this is
    what Search Assist uses as its source.

    No API key required.
    """

    def search(self, query: str, language_code: str = "ru") -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    query,
                    region=f"{language_code}-{language_code}",
                    max_results=5,
                ))
                if not results:
                    return ""
                # Concatenate bodies, return the longest (usually the best)
                bodies = [r.get("body", "") for r in results if r.get("body")]
                if not bodies:
                    return ""
                return max(bodies, key=len)
        except Exception as e:
            print(f"[DDG-SearchAssist] {e}")
            return ""


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper."""
    global _instance
    if _instance is None:
        _instance = DDG_Search_Assist()
    return _instance.search(query, language_code)
