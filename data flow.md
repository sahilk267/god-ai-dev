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
Step 2: API Gateway (routes.py)
┌──────────────────────────────────────────────────────────────────────────────┐
│ POST /api/build → Creates task_id → Returns 202 Accepted                     │
│ GET  /api/status/{id} → Returns progress                                     │
│ WS   /ws/{id} → Live logs streaming                                          │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │
       ▼
Step 3: Task Queue (task_queue.py)
┌──────────────────────────────────────────────────────────────────────────────┐
│ Task added → Queue → Worker picks up → Max 3 concurrent                      │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │
       ▼
Step 4: Orchestrator (orchestrator.py)
┌──────────────────────────────────────────────────────────────────────────────┐
│ run_god_mode(task, project_id):                                              │
│   1. planner.plan(task)           → Get steps                                │
│   2. architect.design_system()    → Get architecture                         │
│   3. coder.build_code()           → Generate code files                      │
│   4. tester.generate_tests()      → Create unit tests                        │
│   5. debugger.fix_errors()        → Auto-fix (max 3 retries)                 │
│   6. reviewer.review_code()       → Quality check                            │
│   7. devops.deploy_app()          → Docker + GitHub                          │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │
       ▼
Step 5: File Manager (file_manager.py)
┌──────────────────────────────────────────────────────────────────────────────┐
│ workspace/project_name/                                                      │
│   ├── app.py                                                                 │
│   ├── models.py                                                              │
│   ├── requirements.txt                                                       │
│   └── Dockerfile                                                             │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │
       ▼
Step 6: Deployment (devops.py + github_service.py)
┌──────────────────────────────────────────────────────────────────────────────┐
│ Docker: docker build → docker run → http://localhost:xxxx                    │
│ GitHub: git init → add → commit → push                                       │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │
       ▼
Step 7: Response (WebSocket)
┌──────────────┐
│ Live logs:   │
│ ✅ Project   │
│    deployed  │
│ 🔗 URL:      │
│    http://.. │
└──────────────┘