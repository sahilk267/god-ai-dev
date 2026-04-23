from backend.core.router import router
from backend.core.experience import experience_service
from backend.core.logger import get_logger
from backend.agents.utils import safe_parse_json
import json

logger = get_logger(__name__)

class MasterAgent:
    async def learn_from_failure(self, project_id: str, logs: list, error: str):
        """Analyze a failure and store the lesson learned"""
        prompt = f"""
        Analyze this failure and extract a 'Lesson Learned'.
        PROJECT ID: {project_id}
        LOGS: {logs[-10:]}
        ERROR: {error}
        
        Return a JSON:
        {{
            "lesson": "Broad principle for next time",
            "fix_pattern": "Specific code pattern that solves this",
            "tags": ["python", "fastapi", "docker"]
        }}
        """
        response = await router.call_primary_llm(prompt, system="You are a Meta-Learning Master Agent")
        
        lesson_doc = safe_parse_json(response)
        if lesson_doc:
            try:
                await experience_service.add_experience(
                    content=f"LESSON: {lesson_doc['lesson']}\nPATTERN: {lesson_doc['fix_pattern']}",
                    metadata={
                        "type": "lesson",
                        "project_id": project_id,
                        "tags": ",".join(lesson_doc.get("tags", []))
                    }
                )
            except Exception as e:
                logger.error(f"Master Agent failed to learn: {e}")
        else:
            logger.warning("Master Agent could not parse lesson from LLM response")

    async def extract_knowledge_from_logs(self, chat_logs: str):
        """Parse external chat logs (Cursor/GPT) into reusable patterns"""
        prompt = f"""
        Extract 3-5 key coding patterns, structural decisions, or library preferences from these chat logs.
        LOGS:
        {chat_logs[:5000]}
        
        Return a JSON array of patterns:
        [{{
            "pattern_name": "Short name",
            "description": "How to implement it",
            "context": "When to use it"
        }}]
        """
        response = await router.call_primary_llm(prompt, system="You are a Knowledge Extraction Expert")
        
        patterns = safe_parse_json(response, fallback=[])
        if not patterns:
            logger.warning("No patterns extracted from logs")
            return 0
            
        for p in patterns:
            try:
                await experience_service.add_experience(
                    content=f"PATTERN: {p['pattern_name']}\nDESC: {p['description']}\nCONTEXT: {p['context']}",
                    metadata={"type": "pattern", "source": "imported_log"}
                )
            except Exception as e:
                logger.error(f"Failed to store pattern: {e}")
        return len(patterns)

    async def get_advice(self, task: str) -> str:
        """Search memory and provide advice for a new task"""
        relevant = await experience_service.query_experience(task, limit=3)
        if not relevant:
            return ""
            
        advice_parts = [r["content"] for r in relevant]
        return "\n\nADVICE FROM PAST EXPERIENCE:\n" + "\n---\n".join(advice_parts)

master_agent = MasterAgent()
