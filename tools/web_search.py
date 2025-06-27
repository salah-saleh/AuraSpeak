from duckduckgo_search import DDGS  # For performing DuckDuckGo web searches


def search_duckduckgo(query, max_results=3):
    """
    Search DuckDuckGo for the given query and return a list of result dicts (title, href, body).
    """
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title", ""),
                "href": r.get("href", ""),
                "body": r.get("body", "")
            })
    return results 