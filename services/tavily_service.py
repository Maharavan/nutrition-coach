from typing import List
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
    results: List[SearchResult] = Field(default_factory=list, description="Normalized search results")


class TavilyService():
    """Service wrapper for querying the Tavily API."""

    def __init__(self):
        """Initialize the TavilyService with a Tavily client."""
        self._client = TavilyClient(api_key=nutrition_config.TAVILY_API_KEY.get_secret_value())

    def search(self, query: str, max_results: int = 5) -> TavilySearchResponse:
        """Search Tavily for the given query and return normalized results."""
        try:
            results = self._client.search(query=query, max_results=max_results)
            search_results = [
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    content=item.get("content", ""),
                )
                for item in results.get("results", [])
            ]  
        except Exception as e:
            logger.exception('Unexpected error %s', str(e))
            search_results = []

        return TavilySearchResponse(query=query, results=search_results)

tavily_service = TavilyService()