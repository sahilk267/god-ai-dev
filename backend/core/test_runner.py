import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any
from .logger import get_logger

logger = get_logger(__name__)

class TestRunner:
    async def run_tests(self, project_path: Path, test_code: str) -> Dict[str, Any]:
        import asyncio
        try:
            test_file = project_path / "test_app.py"
            test_file.write_text(test_code)
            
            process = await asyncio.create_subprocess_exec(
                "pytest", str(test_file), "-v", "--tb=short",
                cwd=str(project_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30.0)
            except asyncio.TimeoutError:
                process.kill()
                return {"success": False, "error": "Tests timed out", "failed": True}
                
            out_decoded = stdout.decode('utf-8', errors='replace')
            err_decoded = stderr.decode('utf-8', errors='replace')
            
            return {
                "success": process.returncode == 0,
                "output": out_decoded[-2000:],
                "error": err_decoded[-2000:],
                "failed": "FAILED" in out_decoded or process.returncode != 0
            }
        except Exception as e:
            return {"success": False, "error": str(e), "failed": True}

test_runner = TestRunner()