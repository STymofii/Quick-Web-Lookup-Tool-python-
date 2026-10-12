import requests
from engines.engine import Engine


class GoogleDictionary(Engine):
    """Free dictionary API — https://dictionaryapi.dev

    No API key required. Works only for single words that exist in the
    dictionary (mostly nouns and common verbs).
    """

    def search(self, query: str, language_code: str = "ru") -> str:
        word = query.strip().split()[0]
        try:
            resp = requests.get(
                f"https://api.dictionaryapi.dev/api/v2/entries/{language_code}/{word}",
                timeout=10,
            )
            if resp.status_code != 200:
                return ""
            data = resp.json()
            r = data[0]
            definition = r["meanings"][0]["definitions"][0]
            return definition.get("definition", "")
        except Exception as e:
            print(f"[GoogleDictionary] {e}")
            return ""


_instance = None


def search(query: str, language_code: str = "ru") -> str:
    global _instance
    if _instance is None:
        _instance = GoogleDictionary()
    return _instance.search(query, language_code)
