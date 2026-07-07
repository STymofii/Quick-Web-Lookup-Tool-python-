import os
from groq import Groq

def search(query: str, language_code: str = "ru") -> str:
    if not os.environ.get("GROQ_API_KEY"):
        return "Error: not found GROQ_API_KEY in .env"

    try:
        client = Groq()
        
        system_prompt = f"You are a database of precise data. Your task is to give the shortest, most concrete answer to a question in the language {language_code}. No politeness, greetings, or unnecessary fluff. Just the bare facts. Examples: for 'capital of France', the answer is 'Paris'; for 'height of the Eiffel Tower', the answer is '330 m'."

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.0
        )
        return completion.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Ошибка Groq: {e}"