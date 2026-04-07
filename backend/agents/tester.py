from backend.core.router import router
from backend.core.logger import get_logger

logger = get_logger(__name__)

async def generate_tests(code_dict: dict) -> str:
    code_samples = "\n\n".join([f"# {path}\n{code[:500]}" for path, code in list(code_dict.items())[:3]])
    
    prompt = f"""
    Write comprehensive unit tests using pytest for this code:
    {code_samples}
    
    Include:
    - Edge cases
    - Error handling tests
    - Mock external dependencies
    - Fixtures
    
    Return ONLY the test code.
    """
    
    tests = await router.call_primary_llm(prompt, system="You are a QA engineer specializing in testing")
    logger.info("Generated test suite")
    return tests