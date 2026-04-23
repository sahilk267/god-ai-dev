"""GitHub integration service"""

import git
import os
from pathlib import Path
from typing import Optional
from backend.core.config import settings
from backend.core.logger import get_logger

logger = get_logger(__name__)

class GitHubService:
    def __init__(self):
        self.token = settings.github_token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def create_repository(self, repo_name: str, description: str = "AI Generated Project") -> Optional[str]:
        """Create a GitHub repository"""
        try:
            import httpx
            url = "https://api.github.com/user/repos"
            data = {
                "name": repo_name,
                "description": description,
                "private": False,
                "auto_init": True
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                repo_url = response.json()["clone_url"]
                logger.info(f"Created repository: {repo_url}")
                return repo_url
            else:
                logger.error(f"Failed to create repo: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"GitHub API error: {e}")
            return None
    
    async def push_to_github(self, project_path: Path, repo_url: str, commit_message: str = "AI generated code") -> bool:
        """Push project to GitHub"""
        try:
            repo = git.Repo.init(project_path)
            
            # Add all files
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            
            # Add remote
            if 'origin' in repo.remotes:
                repo.delete_remote('origin')
            
            origin = repo.create_remote('origin', repo_url)
            
            # Push to main branch
            origin.push(refspec='HEAD:refs/heads/main', force=True)
            
            logger.info(f"Successfully pushed to {repo_url}")
            return True
            
        except Exception as e:
            logger.error(f"Git push failed: {e}")
            return False
    
    async def get_repo_info(self, repo_name: str) -> Optional[dict]:
        """Get repository information"""
        try:
            import httpx
            url = f"https://api.github.com/repos/{repo_name}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            logger.error(f"Failed to get repo info: {e}")
            return None

github_service = GitHubService()