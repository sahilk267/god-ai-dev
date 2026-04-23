# Data flow

End-to-end flow from user prompt to artifacts and optional deploy.  
Cross-check API details in [`api architechture.md`](api%20architechture.md); improvements tracked in [`docs/implementation-plan.md`](docs/implementation-plan.md).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              REQUEST FLOW                                    │
└─────────────────────────────────────────────────────────────────────────────┘

Step 1: User Input
┌──────────────┐
│ "Build a     │
│  todo app"   │
└──────┬───────┘
       │
       ▼
Step 2: API (routes.py) — via Nginx :80 or Uvicorn :8000
┌──────────────────────────────────────────────────────────────────────────────┐
│ POST /api/build → task_queue.add_task → returns { project_id, status: queued } │
│ GET  /api/status/{project_id} → orchestrator.active_projects[project_id]      │
│ WS   /ws/{project_id} → live log frames                                       │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │
       ▼
Step 3: Task queue (task_queue.py)
┌──────────────────────────────────────────────────────────────────────────────┐
│ In-process asyncio.Queue; up to 3 concurrent worker tasks                     │
│ (Redis URL exists in settings for future/optional use — queue is in-memory)   │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │
       ▼
Step 4: Orchestrator (orchestrator.py)
┌──────────────────────────────────────────────────────────────────────────────┐
│ run_god_mode(task, project_id):                                              │
│   Master advice → plan → architect → coder → reviewer loop → tester →         │
│   debugger (retries) → reviewer → devops.deploy_app                           │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │
       ▼
Step 5: File manager (file_manager.py)
┌──────────────────────────────────────────────────────────────────────────────┐
│ workspace/<project_name>/   ← folder name from architecture/coder             │
│   (project_id UUID ≠ folder name — see implementation plan Phase 1–2)         │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │
       ▼
Step 6: Deployment (devops.py + github_service.py)
┌──────────────────────────────────────────────────────────────────────────────┐
│ Docker: build/run when Docker socket available → http://localhost:<port>      │
│ GitHub: create repo + push when token configured                              │
│ If neither: deployment dict may carry url: null (Phase 3–4 messaging)         │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │
       ▼
Step 7: WebSocket + status
┌──────────────┐
│ Live logs +  │
│ final status │
│ (and URL if  │
│  present)    │
└──────────────┘
```

## Additional flows

- **Training**: `POST /api/learn` → Master Agent → ChromaDB (`workspace/.memory`).
- **Editor deploy**: `POST /api/deploy` → `devops_agent` with manually supplied files.

## IDE / local files

Generated code path on host (Compose bind mount): `./workspace/<project_name>/` — see implementation plan **Phase 6**.
