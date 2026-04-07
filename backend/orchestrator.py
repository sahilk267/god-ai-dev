from backend.agents.planner import plan
from backend.agents.architect import design_system
from backend.agents.coder import build_code
from backend.agents.tester import generate_tests
from backend.agents.debugger import fix_errors
from backend.agents.devops import devops_agent
from backend.core.test_runner import test_runner
from backend.core.logger import get_logger
from backend.core.file_manager import file_manager
import asyncio

logger = get_logger(__name__)

class Orchestrator:
    def __init__(self):
        self.active_projects = {}
    
    async def run_god_mode(self, task: str, project_id: str = None) -> dict:
        if not project_id:
            import uuid
            project_id = str(uuid.uuid4())
        
        self.active_projects[project_id] = {"status": "started", "logs": []}
        
        try:
            # Step 1: Planning
            await self._log(project_id, "📋 Planning project...")
            steps = await plan(task)
            
            # Step 2: Architecture
            await self._log(project_id, "🏗️ Designing architecture...")
            architecture = await design_system(task)
            
            # Step 3: Coding
            await self._log(project_id, "💻 Generating code...")
            code_result = await build_code(architecture)
            
            # Step 4: Testing & Debug Loop
            await self._log(project_id, "🧪 Generating and running tests...")
            tests = await generate_tests(code_result["files"])
            
            max_debug_attempts = 3
            for attempt in range(max_debug_attempts):
                test_result = await test_runner.run_tests(
                    file_manager.workspace_dir / code_result["project_name"],
                    tests
                )
                
                if not test_result["failed"]:
                    await self._log(project_id, f"✅ Tests passed!")
                    break
                
                await self._log(project_id, f"⚠️ Tests failed (attempt {attempt + 1}/{max_debug_attempts})")
                
                # Get the main code file to fix
                main_code = code_result["files"].get("app.py", code_result["files"].get("main.py", ""))
                if main_code:
                    fixed_code = await fix_errors(main_code, test_result["error"])
                    file_manager.update_file(code_result["project_name"], "app.py", fixed_code)
                    code_result["files"]["app.py"] = fixed_code
            
            # Step 5: Review
            await self._log(project_id, "🔍 Reviewing code quality...")
            from backend.agents.reviewer import review_code
            review = await review_code(list(code_result["files"].values())[0])
            await self._log(project_id, f"📊 Code score: {review.get('score', 'N/A')}/10")
            
            # Step 6: Deploy
            await self._log(project_id, "🚀 Deploying application...")
            deployment = await devops_agent.deploy_app(
                code_result["project_name"],
                file_manager.workspace_dir / code_result["project_name"]
            )
            
            self.active_projects[project_id]["status"] = "completed"
            await self._log(project_id, f"✨ Project ready! {deployment.get('url', 'Deployed locally')}")
            
            return {
                "success": True,
                "project_id": project_id,
                "project_name": code_result["project_name"],
                "deployment": deployment,
                "review_score": review.get("score")
            }
            
        except Exception as e:
            logger.error(f"Project {project_id} failed: {e}")
            self.active_projects[project_id]["status"] = "failed"
            return {"success": False, "error": str(e), "project_id": project_id}
    
    async def _log(self, project_id: str, message: str):
        self.active_projects[project_id]["logs"].append(message)
        logger.info(f"[{project_id[:8]}] {message}")
        from backend.api.websocket import manager
        import datetime
        await manager.send_to_project(project_id, {
            "type": "log",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat()
        })

orchestrator = Orchestrator()