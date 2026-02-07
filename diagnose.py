# diagnose.py
print("Шаг 1: Импорт base_scraper")
try:
    from base_scraper import BaseScraper
    print("  ✓ Успешно")
except Exception as e:
    print(f"  ✗ Ошибка: {e}")

print("\nШаг 2: Импорт engines.google_snippet")
try:
    from engines import google_snippet
    print("  ✓ Модуль импортирован")
    print(f"  Атрибуты модуля: {dir(google_snippet)}")
    
    if hasattr(google_snippet, 'search'):
        print("  ✓ Функция search найдена")
    else:
        print("  ✗ Функция search НЕ найдена")
except Exception as e:
    print(f"  ✗ Ошибка импорта: {e}")

print("\nШаг 3: Проверка синтаксиса google_snippet.py")
import py_compile
try:
    py_compile.compile('engines/google_snippet.py', doraise=True)
    print("  ✓ Синтаксис корректен")
except py_compile.PyCompileError as e:
    print(f"  ✗ Синтаксическая ошибка: {e}")
