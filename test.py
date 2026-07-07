import time

from dotenv import load_dotenv; load_dotenv()

from engines import groq_snippet
from engines import ddg_groq_snippet



def test():
    engines = [
        ("Groq", groq_snippet.search),
        ("DuckDuckGo-Groq", ddg_groq_snippet.search)
    ]
    while True:
        query = input("Your question: ") 
        if not query:
            break
        for name, search_func in engines:
            start_time = time.time()
            try:
                answer = search_func(query, "ru")
                status = "OK"
            except Exception as e:
                answer = f"[Ошибка: {str(e)[:50]}]"
                status = "FAIL"

            elapsed = time.time() - start_time
            
            print(f"  {name}: {status} - {answer} ({elapsed:.2f}s)")
            if answer and answer != "[Пусто]":
                print(f"    → {answer[:80]}...")



if __name__ == "__main__":
    test()

