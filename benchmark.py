import csv
import time

from dotenv import load_dotenv
load_dotenv()

from test_data import TEST_CASES
from engines.registry import get_engines


def iter_queries():
    for category, questions in TEST_CASES.items():
        for q in questions:
            yield category, q


def run_benchmark():
    engines = get_engines()
    all_queries = list(iter_queries())
    total = len(all_queries)

    print(f"Running benchmark: {total} queries x {len(engines)} engines")
    for name, _ in engines:
        print(f"  - {name}")
    print("=" * 70)

    report = []
    for idx, (category, query) in enumerate(all_queries, 1):
        print(f"\n[{idx}/{total}] [{category}] {query}")
        row = {"ID": idx, "Category": category, "Query": query}
        for name, search_func in engines:
            start = time.time()
            try:
                answer = search_func(query, "ru")
                status = "OK"
            except Exception as e:
                answer = f"[Error: {str(e)[:80]}]"
                status = "FAIL"
            elapsed = time.time() - start
            row[f"{name}_Answer"] = answer if answer else "[Empty]"
            row[f"{name}_Time"] = round(elapsed, 2)
            row[f"{name}_Status"] = status
            print(f"  {name}: {status} ({elapsed:.2f}s)")
        report.append(row)

    if not report:
        print("No data")
        return

    with open("benchmark_results.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=report[0].keys())
        writer.writeheader()
        writer.writerows(report)

    print("\n" + "=" * 70)
    print("Saved to benchmark_results.csv")

    print("\nSTATISTICS:")
    for name, _ in engines:
        success = sum(1 for r in report if r.get(f"{name}_Status") == "OK")
        has_answer = sum(
            1 for r in report
            if r.get(f"{name}_Status") == "OK"
            and r.get(f"{name}_Answer") not in ("", "[Empty]")
        )
        times = [r.get(f"{name}_Time", 0) for r in report]
        avg = sum(times) / len(times) if times else 0
        pct = success / total * 100 if total else 0
        print(f"\n{name}:")
        print(f"  OK: {success}/{total} ({pct:.1f}%)")
        print(f"  Non-empty answers: {has_answer}/{total}")
        print(f"  Avg time: {avg:.2f}s")


if __name__ == "__main__":
    run_benchmark()
