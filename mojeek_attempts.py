"""Mojeek retry attempts with different headers/params.

Reviewer noted: 'our case is home IP, not datacenter'. This script
retries Mojeek with 4 different configurations to see if the block
is IP-based or header-based.
"""
import requests

URL = "https://www.mojeek.com/search"

ATTEMPTS = [
    ("bare requests.get", {"q": "test"}, {}),
    ("Chrome UA + Accept", {"q": "test"}, {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    }),
    ("Firefox UA + Referer", {"q": "test"}, {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
        "Referer": "https://www.mojeek.com/",
        "Connection": "keep-alive",
    }),
    ("with Mojeek=1 cookie", {"q": "test"},
     {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"},
     {"Mojeek": "1"}),
]

for attempt in ATTEMPTS:
    name, params, headers = attempt[0], attempt[1], attempt[2]
    cookies = attempt[3] if len(attempt) > 3 else None
    print(f"\n=== {name} ===")
    try:
        r = requests.get(URL, params=params, headers=headers,
                         cookies=cookies, timeout=15)
        print(f"  status={r.status_code} len={len(r.content)}")
        if len(r.content) > 100:
            print(f"  preview: {r.text[:300]}")
    except Exception as e:
        print(f"  ERROR: {e}")
