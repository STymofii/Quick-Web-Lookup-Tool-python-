import csv
import time
from test_data import TEST_CASES

from dotenv import load_dotenv; load_dotenv()

from engines import groq_engine
from engines import ddg_groq_engine
from engines import wolfram_engine
from engines import serper_engine
#from engines import searchapi_engine
from engines import ddgs_engine


def iter_queries():
    """Разворачивает словарь категорий в плоский список запросов"""
    for category, questions in TEST_CASES.items():
        for q in questions:
            yield category, q


def run_benchmark():
    engines = [
        # ("Groq", groq_engine.search),
        # ("DuckDuckGo-Groq", ddg_groq_engine.search),
        # ("Wolfram", wolfram_engine.search),
        # ("DDGS", ddgs_engine.search)
        ("Serper", serper_engine.search)
    ]

    report = []
    all_queries = list(iter_queries())
    total = len(all_queries)
    
    print(f"Запуск бенчмарка: {total} вопросов x {len(engines)} движков")
    print("=" * 70)

    for idx, (category, query) in enumerate(all_queries, 1):
        print(f"\n[{idx}/{total}] [{category}] {query}")
        row = {"ID": idx, "Категория": category, "Вопрос": query}
        
        for name, search_func in engines:
            start_time = time.time()
            try:
                answer = search_func(query, "ru")
                if not answer:
                    answer = "[Пусто]"
                status = "OK"
            except Exception as e:
                answer = f"[Ошибка: {str(e)[:50]}]"
                status = "FAIL"

            elapsed = time.time() - start_time
            row[f"{name}_Ответ"] = answer
            row[f"{name}_Время_сек"] = round(elapsed, 2)
            row[f"{name}_Статус"] = status
            
            print(f"  {name}: {status} ({elapsed:.2f}s)")
            if answer and answer != "[Пусто]":
                print(f"    → {answer[:80]}...")

        report.append(row)

    if not report:
        print("\nНет данных для записи отчёта")
        return

    # Сохранение результатов
    keys = report[0].keys()
    with open("benchmark_results.csv", "w", newline="", encoding="utf-8-sig") as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(report)

    print("\n" + "=" * 70)
    print("Бенчмарк завершен. Результаты сохранены в benchmark_results.csv")
    print("=" * 70)
    
    # Статистика
    print("\nСТАТИСТИКА:")
    for name, _ in engines:
        success = sum(1 for r in report if r.get(f"{name}_Статус") == "OK")
        has_answer = sum(1 for r in report if r.get(f"{name}_Статус") == "OK" and r.get(f"{name}_Ответ") not in ["[Пусто]", ""])
        times = [r.get(f"{name}_Время_сек", 0) for r in report]
        avg_time = sum(times) / len(times) if times else 0
        
        print(f"\n{name}:")
        print(f"  Успешных запросов: {success}/{total} ({success/total*100:.1f}%)")
        print(f"  С ответами: {has_answer}/{total} ({has_answer/total*100:.1f}%)")
        print(f"  Среднее время: {avg_time:.2f}s")


if __name__ == "__main__":
    run_benchmark()
