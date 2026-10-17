from engines.engine import Engine


class DuckAI(Engine):
    """DuckDuckGo AI Chat (duck.ai) via the p2d-duck library.

    Free, no-account AI chat interface. No API key required.
    This is an LLM, NOT a search engine — answers come from the model's
    parametric memory plus optional injected web search results.

    Requires: pip install p2d-duck
    """

    def __init__(self):
        self._available = None

    def _check(self):
        if self._available is None:
            try:
                from duck_ai import DuckChat, gpt5_mini  # noqa: F401
                self._available = True
            except ImportError:
                self._available = False
        return self._available

    def search(self, query: str, language_code: str = "ru") -> str:
        if not self._check():
            print("[duck.ai] p2d-duck not installed. Run: pip install p2d-duck")
            return ""
        try:
            from duck_ai import DuckChat, gpt5_mini
            with DuckChat(model=gpt5_mini) as chat:
                response = chat.ask(
                    f"Answer in {language_code}. "
                    f"Give the shortest, most precise answer: {query}",
                    web_search=True,
                )
            return (response or "").strip()
        except Exception as e:
            print(f"[duck.ai] {e}")
            return ""


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper."""
    global _instance
    if _instance is None:
        _instance = DuckAI()
    return _instance.search(query, language_code)
