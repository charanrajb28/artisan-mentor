from ddgs.ddgs import DDGS

class WebSearchService:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, keywords: str, max_results: int = 5) -> list[dict]:
        try:
            results = self.ddgs.text(keywords, max_results=max_results)
            return results
        except Exception as e:
            print(f"Error performing web search for '{keywords}': {e}")
            return []
