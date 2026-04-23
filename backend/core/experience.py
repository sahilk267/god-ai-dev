import asyncio
import chromadb
from pathlib import Path
from backend.core.logger import get_logger

logger = get_logger(__name__)

class ExperienceService:
    def __init__(self):
        self.db_path = Path("backend/data/memory")
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name="system_experience",
            metadata={"hnsw:space": "cosine"}
        )

    async def add_experience(self, content: str, metadata: dict):
        """Add a new lesson or pattern to the memory"""
        import uuid
        id = str(uuid.uuid4())

        def _add():
            self.collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[id],
            )

        await asyncio.to_thread(_add)
        logger.info(f"Added experience: {metadata.get('type')} - {id}")

    async def query_experience(self, query: str, limit: int = 5) -> list:
        """Search memory for relevant previous experience"""

        def _query():
            return self.collection.query(
                query_texts=[query],
                n_results=limit,
            )

        results = await asyncio.to_thread(_query)
        
        experiences = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                experiences.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
        return experiences

    async def clear_memory(self):
        """Reset the entire memory collection"""

        def _reset():
            self.client.delete_collection("system_experience")
            return self.client.get_or_create_collection("system_experience")

        self.collection = await asyncio.to_thread(_reset)
        logger.warning("System memory cleared!")

experience_service = ExperienceService()
