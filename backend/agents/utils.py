"""Utility functions shared across agents"""

import json
import re
from backend.core.logger import get_logger

logger = get_logger(__name__)


def strip_json_fences(text: str) -> str:
    """Strip markdown code fences from LLM responses to extract raw JSON.
    
    LLMs often wrap JSON in ```json ... ``` blocks. This function 
    extracts the content inside those fences.
    """
    # Try to find JSON inside ```json ... ``` or ``` ... ```
    pattern = r'```(?:json)?\s*\n?(.*?)\n?\s*```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def safe_parse_json(text: str, fallback=None):
    """Safely parse JSON from an LLM response, handling markdown fences.
    
    Args:
        text: Raw LLM response text
        fallback: Value to return if parsing fails
    
    Returns:
        Parsed JSON object or the fallback value
    """
    cleaned = strip_json_fences(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse JSON from LLM response: {cleaned[:200]}...")
        return fallback
