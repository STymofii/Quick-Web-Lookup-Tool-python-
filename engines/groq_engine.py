from groq import Groq
from engines.engine import Engine


class GroqEngine(Engine):
    """LLM Groq. NOT a search engine. Requires GROQ_API_KEY."""

    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query: str, language_code: str = "ru") -> str:
        if not self.api_key:
            return ""
        try:
            client = Groq(api_key=self.api_key)
            system_prompt = (
                f"You are a database of precise data. Give the shortest, most "
                f"concrete answer in language '{language_code}'. No greetings, "
                f"no fluff."
            )
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
                temperature=0.0,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Groq] {e}")
            return ""


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper. Returns '' if API key is missing."""
    global _instance
    import os
    if not os.getenv("GROQ_API_KEY"):
        return ""
    if _instance is None:
        _instance = GroqEngine(os.getenv("GROQ_API_KEY"))
    return _instance.search(query, language_code)
