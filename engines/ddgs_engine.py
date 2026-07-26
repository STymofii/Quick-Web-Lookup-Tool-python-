from ddgs import DDGS

def search(query: str, language_code: str = "ru") -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region=f"{language_code}-{language_code}", max_results=1))
            
            if results:
                return results[0].get("body", "")
                
    except Exception as e:
        print(f"Error: {e}")
        
    return ""
