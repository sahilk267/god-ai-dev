from backend.core.router import router
from backend.core.logger import get_logger

logger = get_logger(__name__)

async def fix_errors(files_dict: dict, error_log: str) -> dict:
    # Prepare context: include filename and first 1000 chars of each file
    context = ""
    for path, content in list(files_dict.items())[:5]:
        context += f"FILE: {path}\nCONTENT:\n{content[:1000]}\n---\n"
    
    prompt = f"""
    You are a master debugger. Analyze the error and the project context to provide a fix.
    
    PROJECT CONTEXT:
    {context}
    
    ERROR LOG:
    {error_log}
    
    Identify the file that needs fixing and provide the COMPLETE fixed code for that file.
    
    Return JSON:
    {{
        "file_to_fix": "filename.py",
        "fixed_code": "code content",
        "explanation": "what was wrong"
    }}
    """
    
    import json
    response = await router.call_coder_llm(prompt, system="You are an expert full-stack debugger")
    
    try:
        result = json.loads(response)
        logger.info(f"Debugger identified fix in: {result.get('file_to_fix')}")
        return result
    except (Exception, json.JSONDecodeError):
        # Fallback: try to fix based on the first file if JSON fails
        return {
            "file_to_fix": list(files_dict.keys())[0],
            "fixed_code": files_dict[list(files_dict.keys())[0]],
            "explanation": "Debugger fallback"
        }