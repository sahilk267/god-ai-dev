import asyncio
import json
from typing import Optional
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

class ModelRouter:
    def __init__(self):
        self.llm_client = AsyncOpenAI(
            api_key="ollama", # dummy key for local API
            base_url=settings.ollama_base_url
        )
        self._cache = {}

    def _get_cache_key(self, prompt: str, system: str, model: str) -> str:
        import hashlib
        data = f"{model}:{system}:{prompt}"
        return hashlib.md5(data.encode()).hexdigest()
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def call_primary_llm(self, prompt: str, system: str = "You are an expert software architect") -> str:
        cache_key = self._get_cache_key(prompt, system, settings.primary_model)
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        try:
            response = await self.llm_client.chat.completions.create(
                model=settings.primary_model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            result = response.choices[0].message.content
            self._cache[cache_key] = result
            return result
        except Exception as e:
            logger.error(f"Ollama local API error (Primary): {e}")
            from backend.core.exceptions import APICallError
            raise APICallError(f"Ollama local API error: {e}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def call_coder_llm(self, prompt: str, system: str = "You are an expert software engineer") -> str:
        cache_key = self._get_cache_key(prompt, system, settings.coder_model)
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        try:
            response = await self.llm_client.chat.completions.create(
                model=settings.coder_model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=8000
            )
            result = response.choices[0].message.content
            self._cache[cache_key] = result
            return result
        except Exception as e:
            logger.error(f"Ollama local API error (Coder): {e}")
            from backend.core.exceptions import APICallError
            raise APICallError(f"Ollama local API error: {e}")

router = ModelRouter()