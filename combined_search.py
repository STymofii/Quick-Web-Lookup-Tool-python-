"""Fallback chain: try engines in order, return first non-empty answer.

Mirrors the logic of the legacy QA.py:
    voice = search or gdict['short'] or wiki

But using the project's engines and with an explicit priority order.
"""
from engines.ddgs_engine import DDGS_Engine
from engines.google_dictionary import GoogleDictionary
from engines.wikipedia_summary import WikipediaSummary


def search(query: str, language_code: str = "ru") -> tuple[str, str]:
    """Return (answer, source_engine_name)."""
    chain = [
        ("DDGS", DDGS_Engine()),
        ("Wikipedia", WikipediaSummary()),
        ("GoogleDictionary", GoogleDictionary()),
    ]
    for name, engine in chain:
        try:
            ans = engine.search(query, language_code)
            if ans:
                return ans, name
        except Exception:
            continue
    return "", ""


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "Илон Маск"
    ans, src = search(q, "ru")
    print(f"[{src}] {ans}")
