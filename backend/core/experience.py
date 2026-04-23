import chromadb
from pathlib import Path
from backend.core.logger import get_logger
from backend.core.config import settings

logger = get_logger(__name__)

class ExperienceService:
    def __init__(self):
        self.db_path = Path("backend/data/memory")
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        self.collection = self.client.get_or_create_collection(
            name="system_experience",
            metadata={"hnsw:space": "cosine"}
        )

    async def add_experience(self, content: str, metadata: dict):
        """Add a new lesson or pattern to the memory"""
        import uuid
        id = str(uuid.uuid4())
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[id]
        )
        logger.info(f"Added experience: {metadata.get('type')} - {id}")

    async def query_experience(self, query: str, limit: int = 5) -> list:
        """Search memory for relevant previous experience"""
        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        
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
        self.client.delete_collection("system_experience")
        self.collection = self.client.get_or_create_collection("system_experience")
        logger.warning("System memory cleared!")

experience_service = ExperienceService()
