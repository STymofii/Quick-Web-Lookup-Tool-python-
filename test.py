import time

from dotenv import load_dotenv
load_dotenv()

from engines.registry import get_engines


def run_single_engine_test(name, search_func, query):
    start = time.time()
    try:
        answer = search_func(query, "ru")
        status = "OK" if answer else "EMPTY"
    except Exception as e:
        answer = f"[Error: {str(e)[:80]}]"
        status = "FAIL"
    elapsed = time.time() - start
    preview = (answer[:120] + "...") if len(answer) > 120 else answer
    print(f"  {name} [{status}] ({elapsed:.2f}s): {preview}")


def run_engines_test():
    engines = get_engines()
    print(f"Loaded {len(engines)} engines:")
    for name, _ in engines:
        print(f"  - {name}")
    print()
    while True:
        query = input("Your question (empty to exit): ").strip()
        if not query:
            break
        for name, search_func in engines:
            run_single_engine_test(name, search_func, query)


if __name__ == "__main__":
    run_engines_test()
