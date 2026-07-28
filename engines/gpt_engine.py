from g4f import Client

def search(query: str, language_code: str = "ru") -> str:
    """LLM gpt-4o-mini answer. 
    
    Provides answers to the simplest and most common questions.

    Args:
        query (str): The search phrase or question to query (e.g., "Trump age").
        language_code (str, optional): Two-letter ISO language code for the request.

    Returns:
        str: Extracted snippet text from the top search results, or an empty string
            if no matching selectors or content are found.
    """


    system_prompt = f"You are a database of precise data. Your task is to give the shortest, most concrete answer to a question in the language {language_code}. No politeness, greetings, or unnecessary fluff. Do not add sources of information. Just the bare facts. Examples: for 'capital of France', the answer is 'Paris'; for 'height of the Eiffel Tower', the answer is '330 m'. Question:{query}"

    try:        
        client = Client(provider="CopilotApp")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
            ],
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"