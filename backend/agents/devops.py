from backend.core.file_manager import file_manager
from backend.core.logger import get_logger
import docker
import subprocess
from pathlib import Path

logger = get_logger(__name__)

class DevOpsAgent:
    def __init__(self):
        try:
            self.docker_client = docker.from_env()
        except:
            self.docker_client = None
            logger.warning("Docker not available")
    
    async def deploy_app(self, project_name: str, project_path: Path) -> dict:
        deployment_status = {"docker": False, "github": False, "url": None}
        
        # Create Dockerfile
        dockerfile_content = f"""
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || true

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        dockerfile_path = project_path / "Dockerfile"
        dockerfile_path.write_text(dockerfile_content)
        
        # Build and run Docker
        if self.docker_client:
            try:
                image_name = f"ai-app-{project_name}"
                self.docker_client.images.build(path=str(project_path), tag=image_name)
                container = self.docker_client.containers.run(
                    image_name,
                    detach=True,
                    ports={'8000/tcp': None},
                    remove=True
                )
                port = container.attrs['NetworkSettings']['Ports']['8000/tcp'][0]['HostPort']
                deployment_status["docker"] = True
                deployment_status["url"] = f"http://localhost:{port}"
                logger.info(f"Container running on port {port}")
            except Exception as e:
                logger.error(f"Docker deployment failed: {e}")
        
        # GitHub deployment
        try:
            from backend.services.github_service import github_service
            repo_url = await github_service.create_repository(project_name)
            if repo_url:
                success = await github_service.push_to_github(project_path, repo_url)
                deployment_status["github"] = success
                if success:
                    deployment_status["url"] = repo_url
        except Exception as e:
            logger.warning(f"GitHub push failed: {e}")
        
        return deployment_status

devops_agent = DevOpsAgent()