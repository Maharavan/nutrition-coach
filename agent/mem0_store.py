from strands.memory.types import MemoryEntry, SearchOptions,AddMessagesContext
from mem0 import MemoryClient
from config import nutrition_config

class Mem0Store:
    def __init__(self):
        self.client : MemoryClient = MemoryClient(api_key=nutrition_config.MEM0_API_KEY.get_secret_value())

    async def search(self, query: str, options: SearchOptions | None = None):
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