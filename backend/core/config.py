from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434/v1"
    primary_model: str = "qwen2.5-coder:7b"
    coder_model: str = "deepseek-coder:6.7b"
    github_token: Optional[str] = None
    redis_url: str = "redis://localhost:6379"
    workspace_dir: Path = Path("./workspace")
    max_retries: int = 3
    environment: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()
settings.workspace_dir.mkdir(exist_ok=True)