"""One-shot test runner: runs a single query against every engine."""
import sys

from dotenv import load_dotenv
load_dotenv()

from engines.registry import get_engines


def run(query: str):
    for name, fn in get_engines():
        try:
            answer = fn(query, "ru")
        except Exception as e:
            answer = f"[Error: {e}]"
        print(f"{name}: {answer or '[Empty]'}")


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "Столица Исландии"
    run(q)
