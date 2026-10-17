"""Qwant retry with session + cookies from home page.

Tests whether DataDome block can be bypassed by first visiting the main
page to acquire cookies, then calling the API.
"""
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.qwant.com/",
    "Origin": "https://www.qwant.com",
}

s = requests.Session()

print("=== Step 1: visit home page to get cookies ===")
try:
    home = s.get("https://www.qwant.com/", headers=HEADERS, timeout=15)
    print(f"  status={home.status_code} len={len(home.content)}")
    print(f"  cookies: {s.cookies.get_dict()}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n=== Step 2: call API with session cookies ===")
try:
    r = s.get(
        "https://api.qwant.com/v3/search/web",
        params={"q": "test", "count": 1, "locale": "ru_RU",
                "offset": 0, "device": "desktop", "safesearch": 1},
        headers=HEADERS,
        timeout=15,
    )
    print(f"  status={r.status_code} len={len(r.content)}")
    print(f"  body: {r.text[:500]}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n=== Step 3: try Staan (official successor) ===")
try:
    r = requests.get(
        "https://api.staan.ai/v2/search/web",
        params={"q": "test"},
        headers=HEADERS,
        timeout=15,
    )
    print(f"  status={r.status_code}")
    print(f"  body: {r.text[:300]}")
except Exception as e:
    print(f"  ERROR: {e}")
