from backend.core.router import router
from backend.core.file_manager import file_manager
from backend.core.logger import get_logger
import asyncio

logger = get_logger(__name__)

async def build_code(architecture: dict) -> dict:
    files = {}
    
    semaphore = asyncio.Semaphore(5)
    
    async def generate_file(file_path: str, description: str):
        trimmed_architecture = {
            "project_name": architecture.get("project_name", "unknown"),
            "target_file": file_path,
            "architecture_files": list(architecture.get("folder_structure", {}).keys())
        }
        prompt = f"""
        Write production-ready code for {file_path}.
        Description: {description}
        Architecture context: {trimmed_architecture}
        
        Include error handling, logging, and type hints.
        Return ONLY the code without explanations.
        """
        async with semaphore:
            code = await router.call_coder_llm(prompt, system="You are an expert software engineer")
            logger.info(f"Generated: {file_path}")
            return file_path, code

    tasks = []
    for file_path, description in architecture.get("folder_structure", {}).items():
        tasks.append(generate_file(file_path, description))
        
    results = await asyncio.gather(*tasks)
    files = dict(results)
    
    # Save files
    project_name = architecture.get("project_name", "default_project")
    project_path = file_manager.create_project_structure(files, project_name)
    
    return {"files": files, "project_path": str(project_path), "project_name": project_name}