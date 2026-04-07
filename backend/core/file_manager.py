from pathlib import Path
import json
import yaml
from typing import Dict, Any
from .logger import get_logger
from .config import settings
logger = get_logger(__name__)

class FileManager:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir.resolve()
        
    def _safe_path(self, project_name: str, file_path: str = "") -> Path:
        """Resolve and validate path against directory traversal"""
        project_path = (self.workspace_dir / project_name).resolve()
        
        if not str(project_path).startswith(str(self.workspace_dir)):
            raise ValueError(f"Security Alert: Invalid project path traversal detected: {project_name}")
            
        if not file_path:
            return project_path
            
        full_path = (project_path / file_path).resolve()
        if not str(full_path).startswith(str(project_path)):
            raise ValueError(f"Security Alert: Invalid file path traversal detected: {file_path}")
            
        return full_path
    
    def create_project_structure(self, structure: Dict[str, Any], project_name: str):
        project_path = self._safe_path(project_name)
        project_path.mkdir(parents=True, exist_ok=True)
        
        for file_path, content in structure.items():
            full_path = self._safe_path(project_name, file_path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            logger.info(f"Created: {full_path}")
        
        return project_path
    
    def read_file(self, project_name: str, file_path: str) -> str:
        full_path = self._safe_path(project_name, file_path)
        return full_path.read_text() if full_path.exists() else ""
    
    def update_file(self, project_name: str, file_path: str, content: str):
        full_path = self._safe_path(project_name, file_path)
        full_path.write_text(content)
        logger.info(f"Updated: {full_path}")

file_manager = FileManager(settings.workspace_dir)