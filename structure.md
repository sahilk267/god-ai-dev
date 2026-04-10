# Repository structure

```
god-ai-dev/
│
├── 📁 backend/
│   ├── 📄 __init__.py
│   ├── 📄 orchestrator.py              # Pipeline controller
│   │
│   ├── 📁 core/
│   │   ├── 📄 router.py                # LLM (Ollama-compatible)
│   │   ├── 📄 config.py
│   │   ├── 📄 file_manager.py
│   │   ├── 📄 test_runner.py
│   │   ├── 📄 logger.py
│   │   ├── 📄 experience.py            # ChromaDB memory
│   │   └── 📄 exceptions.py
│   │
│   ├── 📁 agents/
│   │   ├── 📄 planner.py
│   │   ├── 📄 architect.py
│   │   ├── 📄 coder.py
│   │   ├── 📄 debugger.py
│   │   ├── 📄 tester.py
│   │   ├── 📄 master.py
│   │   ├── 📄 reviewer.py
│   │   └── 📄 devops.py
│   │
│   ├── 📁 api/
│   │   ├── 📄 routes.py
│   │   └── 📄 websocket.py
│   │
│   ├── 📁 queue/
│   │   ├── 📄 task_queue.py
│   │   └── 📄 worker.py
│   │
│   └── 📁 services/
│       ├── 📄 github_service.py
│       ├── 📄 voice_service.py
│       └── 📄 scraper_service.py
│
├── 📁 frontend/
│   ├── 📄 index.html
│   ├── 📄 style.css
│   ├── 📄 app.js
│   ├── 📄 monaco-editor.html
│   └── 📄 voice-control.js
│
├── 📁 test/
│   ├── 📄 test_orchestrator.py
│   └── 📄 test_agents.py
│
├── 📁 scripts/
│   ├── 📄 setup.sh
│   └── 📄 deploy.sh
│
├── 📁 docker/
│   ├── 📄 Dockerfile                   # Dev backend image (multi-stage)
│   ├── 📄 Dockerfile.backend
│   ├── 📄 Dockerfile.frontend
│   ├── 📄 nginx.conf                 # Used by prod-style compose
│   └── 📄 nginx.dev.conf             # Dev: static + proxy /api /ws /editor
│
├── 📁 docs/
│   └── 📄 implementation-plan.md     # Phased checklist (pipeline + IDE)
│
├── 📁 config/
│   ├── 📄 production.yaml
│   └── 📄 development.yaml
│
├── 📁 workspace/                     # Generated apps + Chroma .memory (gitignored typical)
├── 📁 logs/
│
├── 📄 agent diagram.md               # ASCII agents
├── 📄 api architechture.md           # REST/WS reference
├── 📄 architechture.md               # Mermaid + doc map
├── 📄 data flow.md
├── 📄 db storage architechture.md
├── 📄 deployment architechture.md
│
├── 📄 requirements.txt
├── 📄 .env.example
├── 📄 docker-compose.yml             # Dev: redis, backend, frontend
├── 📄 docker-compose.prod.yml
├── 📄 Makefile
└── 📄 README.md
```

**Canonical details:** avoid duplicating API lists here — use [`api architechture.md`](api%20architechture.md). **Roadmap / checks:** [`docs/implementation-plan.md`](docs/implementation-plan.md).
