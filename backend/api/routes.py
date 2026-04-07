from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from backend.orchestrator import orchestrator
from backend.core.logger import get_logger
import json
from pathlib import Path

app = FastAPI(title="God-Level AI Developer System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

API_KEY_NAME = "X-API-Key"
API_KEY = "god_mode_secret_key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

logger = get_logger(__name__)

class TaskRequest(BaseModel):
    prompt: str


@app.post("/api/build")
async def build_project(request: TaskRequest, api_key: str = Depends(get_api_key)):
    from backend.queue.task_queue import task_queue
    project_id = await task_queue.add_task(request.prompt)
    return {"project_id": project_id, "status": "queued"}

@app.get("/api/status/{project_id}")
async def get_status(project_id: str):
    if project_id in orchestrator.active_projects:
        return orchestrator.active_projects[project_id]
    return {"status": "not_found"}

@app.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    from backend.api.websocket import manager
    import datetime
    client_id = await manager.connect(websocket, project_id)
    
    # Send existing logs
    if project_id in orchestrator.active_projects:
        for log in orchestrator.active_projects[project_id]["logs"]:
            await manager.send_to_project(project_id, {
                "type": "log",
                "message": log,
                "timestamp": datetime.datetime.now().isoformat()
            })
    
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(client_id, project_id)

@app.get("/api/projects")
async def list_projects():
    return list(orchestrator.active_projects.keys())

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/metrics")
async def metrics():
    return {
        "active_projects": len(orchestrator.active_projects),
        "status": "healthy"
    }

@app.delete("/api/projects/{project_id}")
async def cancel_project(project_id: str):
    from backend.queue.task_queue import task_queue
    cancelled = await task_queue.cancel_task(project_id)
    if project_id in orchestrator.active_projects:
        orchestrator.active_projects[project_id]["status"] = "cancelled"
        return {"status": "cancelled", "project_id": project_id}
    return {"status": "not_found"}

from fastapi.background import BackgroundTask
import shutil

@app.get("/api/projects/{project_id}/download")
async def download_project(project_id: str):
    from backend.core.file_manager import file_manager
    try:
        project_path = file_manager._safe_path(project_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Project not found")
        
    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project empty")
        
    zip_path = file_manager.workspace_dir / f"{project_id}.zip"
    shutil.make_archive(str(file_manager.workspace_dir / project_id), 'zip', str(project_path))
    
    return FileResponse(
        path=zip_path,
        filename=f"{project_id}.zip",
        media_type="application/zip",
        background=BackgroundTask(lambda: zip_path.unlink(missing_ok=True))
    )

@app.get("/editor")
async def serve_editor():
    editor_path = Path(__file__).parent.parent.parent / "frontend" / "monaco-editor.html"
    if editor_path.exists():
        return FileResponse(editor_path)
    return {"message": "Editor not found"}

@app.get("/api/files")
async def get_files():
    from backend.core.file_manager import file_manager
    files = {}
    if file_manager.workspace_dir.exists():
        import os
        for root, _, filenames in os.walk(file_manager.workspace_dir):
            for file in filenames:
                if file.endswith(('.py', '.html', '.js', '.css', '.json', '.txt', '.md')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, file_manager.workspace_dir)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            files[rel_path] = f.read()
                    except:
                        pass
    return {"files": files}

class DeployRequest(BaseModel):
    files: dict
    main_file: str = None

@app.post("/api/deploy")
async def deploy_editor_files(request: DeployRequest, api_key: str = Depends(get_api_key)):
    from backend.agents.devops import devops_agent
    from backend.core.file_manager import file_manager
    import uuid
    project_name = f"manual-{uuid.uuid4().hex[:6]}"
    project_path = file_manager.create_project_structure(request.files, project_name)
    deployment = await devops_agent.deploy_app(project_name, project_path)
    
    if deployment.get("docker") or deployment.get("url"):
        return {"success": True, "url": deployment.get("url", "Deployed locally")}
    return {"success": False, "error": "Deployment failed"}

from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
async def startup_event():
    from backend.queue.worker import background_worker
    await background_worker.start(orchestrator)

@app.on_event("shutdown")
async def shutdown_event():
    from backend.queue.worker import background_worker
    await background_worker.stop()

@app.get("/")
async def serve_frontend():
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "index.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    return {"message": "God-Level AI Developer System is running!"}