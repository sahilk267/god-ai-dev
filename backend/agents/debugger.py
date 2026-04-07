from backend.core.router import router
from backend.core.logger import get_logger

logger = get_logger(__name__)

async def fix_errors(code: str, error_log: str) -> str:
    prompt = f"""
    Fix the errors in this code:
    
    CODE:
    {code[:2000]}
    
    ERROR:
    {error_log}
    
    Provide the complete fixed code with explanations of what was changed.
    """
    
    fixed_code = await router.call_coder_llm(prompt, system="You are a debugging expert")
    logger.info("Attempted to fix errors")
    return fixed_code