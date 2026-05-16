from smolagents import tool
from ddgs import DDGS


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo and return a summary of results.
    
    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default 5).
    
    Returns:
        A formatted string of search results with titles, URLs, and snippets.
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            if not results:
                return "No results found."
            
            formatted = []
            for i, r in enumerate(results, 1):
                formatted.append(f"{i}. {r['title']}\n   URL: {r['href']}\n   {r['body']}\n")
            return "\n".join(formatted)
    except Exception as e:
        return f"Search error: {e}"
