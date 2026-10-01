from ddgs import DDGS
from engines.engine import Engine

class DDGS_Engine(Engine):
    def search(self, query: str, language_code: str = "ru") -> str:
        """Search with DDGS library.

        Works well, producing acceptable results without limitations

        Args:
            query (str): The search phrase or question to query (e.g., "Trump age").
            language_code (str, optional): Two-letter ISO language code for the request.

        Returns:
            str: Extracted snippet text from the top search results, or an empty string
                if no matching selectors or content are found.
        """

        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, region=f"{language_code}-{language_code}", max_results=1))
            
                if results:
                    return results[0].get("body", "")
                
        except Exception as e:
            print(f"Error: {e}")
        
        return ""


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper."""
    global _instance
    if _instance is None:
        _instance = DDGS_Engine()
    return _instance.search(query, language_code)
