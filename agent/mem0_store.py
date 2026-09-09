from functools import lru_cache
import logging
from strands.memory.types import MemoryEntry, SearchOptions, AddMessagesContext
from mem0 import MemoryClient
from config import nutrition_config
from strands.memory import MemoryManager
logger = logging.getLogger(__name__)

class Mem0Store:
    def __init__(self, user_id: str, client: MemoryClient):
        self.user_id = user_id
        self.client = client


    async def search(self, query: str, options: SearchOptions | None = None):
        if self.client is None:
            return []
        results = self.client.search(query=query, user_id=self.user_id)
        limits = options.max_search_results if options else len(results)

        return [
            MemoryEntry(
                content=res["fact"],
                metadata={"id": res["id"], "score": res.get("score", 1.0)}
            )
            for res in results[:limits]
        ]

    def _format_message(self, content: str, role: str) -> dict[str, str]:
        if content is None:
            raise ValueError("Content cannot be None")

        if role not in {"user", "assistant"}:
            raise ValueError(f"Unsupported role: {role}")

        return {
            "role": role,
            "content": content,
        }
    
    async def add_messages(self,content: AddMessagesContext | None = None) -> None:
        if self.client is None:
            logger.warning("Mem0 client not configured; skipping add_messages.")
            return
        if content is None or not content.messages:
            logger.warning("No messages provided to add to Mem0 store.")
            return

        messages = [
            self._format_message(message.content, message.role) for message in content.messages
        ]
        try:
            self.client.add(
                user_id=self.user_id,
                messages=messages
            )
        except Exception as e:
            logger.error("Failed to add messages to Mem0 store: %s", e)

class Mem0Service:
    def __init__(self):
        self.client: MemoryClient
        try:
            self.client = MemoryClient(api_key=nutrition_config.get_mem0_api_key())
        except ValueError:
            logger.warning("Mem0 API key is not configured. Memory features will be unavailable until MEM0_API_KEY is set.")
            raise
    def get_memory_manager(self,user_id: str) -> MemoryManager:
        store = Mem0Store(user_id=user_id, client=self.client)
        return MemoryManager(stores=[store])

@lru_cache()
def get_mem0_store() -> Mem0Service:
    """Get a cached instance of the Mem0Service."""
    return Mem0Service()