"""Attempts to bypass DDG snippet limitations.

Tests 7 different endpoints/parameter combinations to see if a working
short-answer endpoint exists. Result stored as evidence for REPORT.md.
"""
import requests

QUERIES = ["capital of France", "who is Pushkin"]

ENDPOINTS = [
    ("api.duckduckgo.com basic", "https://api.duckduckgo.com/",
     {"q": "{q}", "format": "json", "no_html": 1}),
    ("api.duckduckgo.com skip_disambig", "https://api.duckduckgo.com/",
     {"q": "{q}", "format": "json", "no_html": 1, "skip_disambig": 1}),
    ("api.duckduckgo.com t=quicklook", "https://api.duckduckgo.com/",
     {"q": "{q}", "format": "json", "t": "quicklook"}),
    ("api.duckduckgo.com kl=ru-ru", "https://api.duckduckgo.com/",
     {"q": "{q}", "format": "json", "kl": "ru-ru"}),
    ("duckduckgo.com/html/ scrape", "https://duckduckgo.com/html/",
     {"q": "{q}"}),
    ("html.duckduckgo.com/html/ scrape", "https://html.duckduckgo.com/html/",
     {"q": "{q}", "kl": "ru-ru"}),
    ("lite.duckduckgo.com/lite/ scrape", "https://lite.duckduckgo.com/lite/",
     {"q": "{q}", "kl": "ru-ru"}),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}

for name, url, base_params in ENDPOINTS:
    print(f"\n=== {name} ===")
    for q in QUERIES:
        params = {k: v.replace("{q}", q) if isinstance(v, str) else v
                  for k, v in base_params.items()}
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=15)
            print(f"  [{q}] status={r.status_code} len={len(r.content)}")
            if "api.duckduckgo" in url:
                try:
                    d = r.json()
                    print(f"    Answer={d.get('Answer')!r}")
                    print(f"    AbstractText={(d.get('AbstractText') or '')[:60]!r}")
                    print(f"    RelatedTopics={len(d.get('RelatedTopics', []))}")
                except Exception:
                    print(f"    non-JSON: {r.text[:200]}")
            else:
                print(f"    preview: {r.text[:200].replace(chr(10), ' ')}")
        except Exception as e:
            print(f"  [{q}] ERROR {e}")
