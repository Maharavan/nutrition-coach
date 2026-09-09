import logging

from strands.memory.types import MemoryEntry, SearchOptions, AddMessagesContext
from mem0 import MemoryClient
from config import nutrition_config

logger = logging.getLogger(__name__)

class Mem0Store:
    def __init__(self):
        self.client: MemoryClient | None = None
        try:
            self.client = MemoryClient(api_key=nutrition_config.get_mem0_api_key())
        except ValueError:
            logger.warning(
                "Mem0 API key is not configured. Memory features will be unavailable until MEM0_API_KEY is set."
            )

    async def search(self, query: str, options: SearchOptions | None = None):
        if self.client is None:
            return []
        results = self.client.search(query=query)
        limits = options.max_search_results if options else len(results)

        return [
            MemoryEntry(
                content=res["fact"],
                metadata={"id": res["id"], "score": res.get("score", 1.0)}
            )
            for res in results[:limits]
        ]

    async def add_messages(self,content: AddMessagesContext | None = None) -> None:
        self.client.add(content)

def get_mem0_store() -> Mem0Store:
    return Mem0Store()