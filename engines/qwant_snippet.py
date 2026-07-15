import json
from base_scraper import BaseScraper


def search(query: str, language_code: str = "ru") -> str:
    scraper = BaseScraper()
    url = "https://api.qwant.com/v3/search/web"

    params = {
        "q": query,
        "locale": f"{language_code}_{language_code.upper()}",
        "count": 5,
        "t": "web",
    }
    
    data = scraper.fetch_json(url, params)
    print(data)

    if data.get("status") == "success":
        result_data = data.get("data", {})

        if "instant_answers" in result_data and result_data["instant_answers"]:
            answer = result_data["instant_answers"][0]
            return answer.get("content", "").strip()

        items = result_data.get("result", {}).get("items", [])
        if items:
            first_item = items[0]
            return first_item.get("desc", "").strip()

    return ""