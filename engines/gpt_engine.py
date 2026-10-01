from g4f import Client
from engines.engine import Engine


class GPT_Engine(Engine):
    """LLM via g4f (provider=CopilotApp). NOT a search engine.

    Unreliable: at the time of testing the CopilotApp provider returned
    HTTP 460 on every query. Kept as a stub; returns empty string on error.
    """

    def search(self, query: str, language_code: str = "ru") -> str:
        system_prompt = (
            f"You are a database of precise data. Give the shortest, most "
            f"concrete answer in language '{language_code}'. No greetings, "
            f"no sources, no fluff. Examples: 'capital of France' -> 'Paris'."
        )
        try:
            client = Client(provider="CopilotApp")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[GPT-4o] {e}")
            return ""


# ---- module-level interface required by the task ----
_instance = None

def search(query: str, language_code: str = "ru") -> str:
    """Module-level wrapper."""
    global _instance
    if _instance is None:
        _instance = GPT_Engine()
    return _instance.search(query, language_code)
