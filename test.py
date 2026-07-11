import time
from urllib.parse import quote_plus
from typing import Callable

from dotenv import load_dotenv; load_dotenv()

from base_scraper import BaseScraper
#from engines import groq_snippet
#from engines import ddg_groq_engine
#from engines import wolfram_engine
#from engines import google_snippet
#from engines import ddg_snippet
from engines import qwant_snippet

def run_single_engine_test(name: str, search_func: Callable[[str, str], None], query: str):
    start_time = time.time()
    try:
        answer = search_func(query, "en")
        status = "OK"
    except Exception as e:
        answer = f"[Ошибка: {str(e)[:50]}]"
        status = "FAIL"

    elapsed = time.time() - start_time
            
    print(f"  {name}: {status} - {answer} ({elapsed:.2f}s)")
    #if answer and answer != "[Пусто]":
        #print(f"    → {answer[:80]}...")

def run_engines_test():
    engines = [
        #("Groq", groq_snippet.search),
        #("DuckDuckGo-Groq", ddg_groq_snippet.search),
        #("Wolfram", wolfram_engine.search),
        # ("DuckDuckGo", ddg_snippet.search),
        ("Qwant", qwant_snippet.search)

    ]
    while True:
        query = input("Your question: ") 
        if not query:
            break
        for name, search_func in engines:
            run_single_engine_test(name, search_func, query) 


def test():
    run_engines_test()


if __name__ == "__main__":
    test()

