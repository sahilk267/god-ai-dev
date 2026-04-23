from backend.core.router import router
from backend.core.logger import get_logger
from backend.agents.utils import safe_parse_json

logger = get_logger(__name__)

async def review_code(code: str) -> dict:
    prompt = f"""
    Review this code and provide improvements:
    {code[:2000]}
    
    Return JSON:
    {{
        "score": "1-10",
        "issues": ["issue1", "issue2"],
        "suggestions": ["suggestion1", "suggestion2"],
        "optimized_code": "improved version"
    }}
    """
    
    response = await router.call_primary_llm(prompt, system="You are a senior code reviewer")
    
    fallback = {
        "score": 7,
        "issues": ["Consider adding error handling", "Add type hints"],
        "suggestions": ["Implement logging", "Add docstrings"],
        "optimized_code": code
    }
    
    review = safe_parse_json(response, fallback=fallback)
    logger.info(f"Code review score: {review.get('score')}")
    return review