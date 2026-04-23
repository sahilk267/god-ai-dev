from backend.core.router import router
from backend.core.logger import get_logger
from backend.agents.utils import safe_parse_json

logger = get_logger(__name__)

async def plan(task: str) -> list:
    prompt = f"""
    Break down this software development task into 5-7 clear steps:
    Task: {task}
    
    Return ONLY a JSON array of steps, each with 'step_number', 'description', and 'estimated_time'.
    Example: [{{"step_number":1,"description":"Setup project structure","estimated_time":"30min"}}]
    """
    
    response = await router.call_primary_llm(prompt, system="You are a software project planner")
    
    fallback = [
        {"step_number": 1, "description": "Analyze requirements", "estimated_time": "10min"},
        {"step_number": 2, "description": "Design architecture", "estimated_time": "20min"},
        {"step_number": 3, "description": "Implement core features", "estimated_time": "1hr"},
        {"step_number": 4, "description": "Write tests", "estimated_time": "30min"},
        {"step_number": 5, "description": "Deploy application", "estimated_time": "15min"}
    ]
    
    steps = safe_parse_json(response, fallback=fallback)
    logger.info(f"Planned {len(steps)} steps")
    return steps