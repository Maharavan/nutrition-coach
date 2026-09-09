import logging
from pydantic import BaseModel, Field

from tavily import TavilyClient
from config import nutrition_config

logger = logging.getLogger(__name__)

class SearchResult(BaseModel):
    """A single normalized Tavily search result."""
    title: str
    url: str
    content: str


class TavilySearchResponse(BaseModel):
    """Result of a Tavily search query."""
    query: str = Field(..., description="The query that was searched")
    results: str = Field(..., description="Formatted search-result context, ready to use as LLM input")


class TavilyService():
    """Service wrapper for querying the Tavily API."""

    def __init__(self):
        """Initialize the TavilyService with a Tavily client."""
        self._client = None
        try:
            self._client = TavilyClient(api_key=nutrition_config.get_tavily_api_key())
        except ValueError:
            logger.warning(
                "Tavily API key is not configured. Search calls will return no results until TAVILY_API_KEY is set."
            )

    def search(self, query: str, max_results: int = 5) -> TavilySearchResponse:
        """Search Tavily for the given query and return a formatted context string."""
        if self._client is None:
            logger.warning("Tavily search skipped because the API key is missing.")
            return TavilySearchResponse(query=query, results="")

        try:
            response = self._client.search(query=query, max_results=max_results)
            search_results = [
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    content=item.get("content", ""),
                )
                for item in response.get("results", [])
            ]
            context = self.build_search_context(results=search_results)
        except Exception as e:
            logger.exception('Unexpected error %s', str(e))
            context = ""

        return TavilySearchResponse(query=query, results=context)
    
    def build_search_context(self, results: list[SearchResult]) -> str:
        """Build a formatted context string from search results.

        Args:
            results: List of search results to format.

        Returns:
            Formatted string combining all search results.
        """
        return "\n\n".join(
            f"Source: {result.title}\n"
            f"URL: {result.url}\n"
            f"{result.content}"
            for result in results
        )


tavily_service = TavilyService()