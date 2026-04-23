# API architecture

HTTP and WebSocket surface for the God-Level AI Developer System.  
Canonical checklist for API-related work: [`docs/implementation-plan.md`](docs/implementation-plan.md) (Phases 1–3, 6).

## Authentication

| Header | When required |
|--------|----------------|
| `X-API-Key: god_mode_secret_key` | `POST /api/build`, `POST /api/learn`, `POST /api/deploy` |

Public or key-optional routes use `APIKeyHeader` with `auto_error=False` only where implemented in `backend/api/routes.py`.

## REST and WebSocket

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/api/build` | Queue build; returns `{ project_id, status }` (task UUID) | API key |
| POST | `/api/learn` | Train Master Agent from logs or URL | API key |
| GET | `/api/status/{project_id}` | Project status and logs | None |
| GET | `/api/projects` | List active `project_id` keys | None |
| DELETE | `/api/projects/{project_id}` | Cancel if pending | None |
| GET | `/api/projects/{project_id}/download` | ZIP of project artifacts | None |
| GET | `/api/health` | Liveness | None |
| GET | `/api/metrics` | App metrics summary | None |
| GET | `/api/files` | Workspace file listing (editor) | None |
| POST | `/api/deploy` | Deploy files from editor flow | API key |
| GET | `/editor` | Monaco editor page | None |
| GET | `/` | Serves `frontend/index.html` when present | None |
| WS | `/ws/{project_id}` | Live log stream for that task id | None |

Prometheus instrumentator may expose additional metrics routes as configured in `routes.py`.

## Development vs direct backend

| Access | URL base | Notes |
|--------|----------|--------|
| Docker Compose (recommended) | `http://localhost` (port **80**) | Nginx proxies `/api/*`, `/ws/*`, `/editor` to backend **8000**; static UI from `frontend/`. |
| Local `make dev` | `http://localhost:8000` | Uvicorn only; hit API and WebSocket on **8000**. |

## Project identity (implementation plan)

- **`project_id`**: UUID used in `/api/projects`, `/ws/...`, `/api/status/...`, and queue/orchestrator state.
- **`project_name`**: Folder name under `workspace/` where generated files live (from architect/coder).  
  **Phases 1–2** of [`docs/implementation-plan.md`](docs/implementation-plan.md) align download and status metadata with this split.

## Related docs

- [`data flow.md`](data%20flow.md) — request path through queue and orchestrator.
- [`deployment architechture.md`](deployment%20architechture.md) — prod vs dev topology.
