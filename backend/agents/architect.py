from backend.core.router import router
from backend.core.logger import get_logger
import json

logger = get_logger(__name__)

async def design_system(task: str) -> dict:
    prompt = f"""
    Design complete system architecture for: {task}
    
    Return a JSON with:
    {{
        "project_name": "string",
        "folder_structure": {{
            "backend/main.py": "FastAPI entry point",
            "backend/models.py": "Database models",
            "backend/routes.py": "API endpoints",
            "frontend/index.html": "UI",
            "docker/Dockerfile": "Container config",
            "requirements.txt": "Dependencies"
        }},
        "database": {{
            "type": "postgresql/sqlite/mongodb",
            "tables": ["users", "products", "orders"]
        }},
        "apis": ["/api/auth", "/api/data", "/api/health"],
        "frontend_framework": "React/Vanilla JS"
    }}
    """
    
    response = await router.call_primary_llm(prompt, system="You are a senior system architect")
    
    try:
        architecture = json.loads(response)
        logger.info(f"Designed system: {architecture.get('project_name')}")
        return architecture
    except (Exception, json.JSONDecodeError):
        # Fallback architecture
        return {
            "project_name": "ai_generated_app",
            "folder_structure": {
                "app.py": "# Main application\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef root():\n    return {{'message': 'Hello World'}}",
                "requirements.txt": "fastapi\nuvicorn"
            },
            "database": {"type": "sqlite", "tables": ["items"]},
            "apis": ["/", "/health"],
            "frontend_framework": "Vanilla JS"
        }