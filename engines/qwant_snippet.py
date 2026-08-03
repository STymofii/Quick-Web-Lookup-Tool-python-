import json
from base_scraper import BaseScraper
from engines.engine import Engine

class QwantSnippet(Engine):
    def search(self, query: str, language_code: str = "ru") -> str:
        """Search in Qwant.

        !!!DOESN'T WORK DUE TO ANTIBOT CHECK!!!

        Args:
            query (str): The search phrase or question to query (e.g., "Trump age").
            language_code (str, optional): Two-letter ISO language code for the request.

        Returns:
            str: Extracted snippet text from the top search results, or an empty string
                if no matching selectors or content are found.
        """

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