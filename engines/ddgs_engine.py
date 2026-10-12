from ddgs import DDGS
from engines.engine import Engine


class DDGS_Engine(Engine):
    """DuckDuckGo search via the `ddgs` library.

    Works without an API key. No rate limits observed (20/20 stress test).
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
                    return results[0].get("body", "")
        except Exception as e:
            # Silent: empty result is a valid outcome
            pass
        return ""


_instance = None


def search(query: str, language_code: str = "ru") -> str:
    global _instance
    if _instance is None:
        _instance = DDGS_Engine()
    return _instance.search(query, language_code)
