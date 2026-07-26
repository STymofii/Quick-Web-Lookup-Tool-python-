import time
from urllib.parse import quote_plus
from typing import Callable

from dotenv import load_dotenv; load_dotenv()

from base_scraper import BaseScraper

from engines import groq_engine
from engines import ddg_groq_engine
from engines import wolfram_engine
from engines import serper_engine
from engines import searchapi_engine
from engines import ddgs_engine


def run_single_engine_test(name: str, search_func: Callable[[str, str], None], query: str):
    start_time = time.time()
    try:
        answer = search_func(query, "ru")
        if not answer:
            raise Exception("Answer is empty")
        status = "OK"
    except Exception as e:
        answer = f"[Error: {str(e)[:50]}]"
        status = "FAIL"

    elapsed = time.time() - start_time
            
    #print(f"  {name}: {status} - {answer} ({elapsed:.2f}s)")
    if answer and answer != "[Пусто]":
        print(f"    {name} ({elapsed:.2f}s):\n{answer[:80] + '...' if len(answer) > 80 else answer}")

def run_engines_test():
    engines = [
        ("Groq", groq_engine.search),
        ("DuckDuckGo-Groq", ddg_groq_engine.search),
        ("Wolfram", wolfram_engine.search),
        ("Serper", serper_engine.search),
        ("SearchAPI", searchapi_engine.search),
        ("DDGS", ddgs_engine.search),

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

