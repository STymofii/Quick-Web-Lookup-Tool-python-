import os
from groq import Groq
from ddgs import DDGS
from engines.engine import Engine

class DDG_Groq_Engine(Engine):
    def __init__(self, api_key):
        """
        Args:
            api_key (str): os.environ.get(GROQ_API_KEY).
        """
        self.api_key=api_key

    def get_web_search_results(self, query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if not results:
                    return ""
                context = "\n".join([f"{r['title']}: {r['body']}" for r in results])
                return context
        except Exception:
            return ""

    def search(self, query: str, language_code: str = "ru") -> str:
        """Search on DDGS library and transfer search results to LLM Groq.

        Works well, producing acceptable results without limitations, but LLM does not meet the project requirements

        Args:
            query (str): The search phrase or question to query (e.g., "Trump age").
            language_code (str, optional): Two-letter ISO language code for the request.

        Returns:
            str: LLM answer text from the top search results, or an empty string
                if no matching selectors or content are found.
        """

        web_context = self.get_web_search_results(query)
        #print(f"DDG Search result: {web_context}")
    
        if not web_context:
            web_context = "No data found online. Answer based on your knowledge."

        try:
            client = Groq()
        
            system_prompt = f"You are a data verifier. Your only task is to read the provided context from the internet and extract from it the shortest, most precise answer to the user's question. Answer strictly in {language_code}. No greetings, no politeness, no unnecessary words. Just the bare facts (number, name, date). If there are contradictions in the context, choose the most recent or authoritative fact. Try to extract data from context as accurately as possible if available."

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Query: {query}"}
                ],
                temperature=0.0
            )
        
            return completion.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Ошибка Groq: {e}"