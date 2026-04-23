# 🤖 God-Level AI Developer System

## 🚀 Complete Autonomous Software Factory

Transform any idea into production-ready code in minutes using AI agents.

### ✨ Features

- **One Prompt → Full SaaS** - Describe your app, get complete code
- **Multi-Agent Architecture** - Master, Planner, Architect, Coder, Tester, DevOps
- **Master Agent Training** - Learns from your patterns and previous builds
- **URL-Based Memory** - Import knowledge directly from ChatGPT/Cursor share links
- **Reflection Loop** - Self-auditing code before testing
- **Auto Test Generation** - Unit tests written automatically
- **Project-Wide Debugging** - Complex traces across multiple files automatically
- **Self-Healing** - Detects and fixes errors automatically
- **Docker Deployment** - One-click container deployment (when Docker is available to the backend)
- **GitHub Integration** - Auto push to GitHub
- **Voice Control** - Build apps with voice commands (Hindi/English)
- **Real-time Logs** - WebSocket streaming of build process
- **Monaco Editor** - VS Code-like editing experience

### 📚 Architecture and API

| Doc | Purpose |
|-----|---------|
| [docs/implementation-plan.md](docs/implementation-plan.md) | Checklist: pipeline fixes (download, deploy messaging, tests, IDE path) |
| [architechture.md](architechture.md) | Mermaid overview + doc map |
| [api architechture.md](api%20architechture.md) | Endpoints, auth, ports 80 vs 8000 |
| [data flow.md](data%20flow.md) | Queue → orchestrator → workspace |
| [deployment architechture.md](deployment%20architechture.md) | Docker Compose dev vs prod |
| [structure.md](structure.md) | Repository layout |

### 📦 Quick Start (local Python)

```bash
# Clone and setup
git clone <repo-url>
cd god-ai-dev

# Install dependencies
make install

# Configure environment
cp .env.example .env
# Edit .env: models (Qwen2.5-Coder, DeepSeek-Coder), REDIS_URL, OLLAMA_BASE_URL as needed

# Run API only (no Docker)
make dev

# Open API / served UI
# http://localhost:8000
```

### 🐳 Full stack (Docker Compose — recommended)

Requires **Docker** and free ports **80**, **8000**, **6379**.

```bash
cp .env.example .env   # if .env missing
docker compose up -d --build
```

- **UI + proxied API:** http://localhost (Nginx → backend)
- **API direct:** http://localhost:8000
- **Health:** http://localhost:8000/api/health

**Ollama:** Backend expects a local LLM at `OLLAMA_BASE_URL` (default uses `host.docker.internal` on Docker Desktop). Pull models matching `.env` (e.g. `qwen2.5-coder:7b`).

**Generated projects on disk:** `./workspace/<project_name>/` (bind-mounted into the backend). Use Cursor/VS Code → Open Folder on that path. Further IDE steps: [docs/implementation-plan.md](docs/implementation-plan.md) Phase 6.

### 🔧 Makefile

`make help` — install, dev, build (`docker compose build`), deploy script, test, clean.
