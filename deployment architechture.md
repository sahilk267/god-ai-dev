# Deployment architecture

## Development (docker-compose.yml)

Typical laptop stack:

| Service | Role | Host port |
|---------|------|-----------|
| **redis** | Redis server (configured; queue is in-process today) | 6379 |
| **backend** | FastAPI + Uvicorn | 8000 |
| **frontend** | Nginx: static `frontend/` + **reverse proxy** to backend | 80 |

- Nginx config: `docker/nginx.dev.conf` — proxies `/api/`, `/ws/`, `/editor` to `backend:8000`.
- Backend **does not** use `--reload` in Compose (stable WebSockets; rebuild image for code changes).
- Volumes: `./workspace`, `./logs` mounted into backend.

**Docker-from-container:** Backend logs may show *Docker not available* unless the host Docker socket is mounted. Then DevOps agent cannot run local containers; deploy `url` may be `null` unless GitHub succeeds. Tracked in [`docs/implementation-plan.md`](docs/implementation-plan.md) Phase 4.

## Production-style (docker-compose.prod.yml)

Higher-level diagram (scaling, Prometheus, Grafana, TLS nginx) — see that file for services and networks. May use multiple backend replicas and external nginx on 443; align volumes and env with your ops runbook.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PRODUCTION (REFERENCE)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                           ┌─────────────┐                                   │
│                           │   USER      │                                   │
│                           └──────┬──────┘                                   │
│                                  │                                          │
│                           ┌──────▼──────┐                                   │
│                           │   NGINX     │  Port 80/443                       │
│                           │  (Reverse   │                                   │
│                           │   Proxy)    │                                   │
│                           └──────┬──────┘                                   │
│                                  │                                          │
│                  ┌───────────────┼───────────────┐                          │
│                  │               │               │                          │
│            ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐                    │
│            │ Backend   │   │ Backend   │   │  Redis    │                    │
│            │ (replica) │   │ (replica) │   │  :6379    │                    │
│            └─────┬─────┘   └─────┬─────┘   └──────────┘                    │
│                  │               │                                          │
│            ┌─────▼─────┐   ┌─────▼─────┐                                    │
│            │ workspace │   │   logs    │   (+ prometheus/grafana per compose)│
│            │  volume   │   │  volume   │                                    │
│            └───────────┘   └───────────┘                                    │
│                                                                              │
│  See docker-compose.prod.yml for exact service names and networks.          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Related

- [`api architechture.md`](api%20architechture.md) — ports 80 vs 8000.
- [`docs/implementation-plan.md`](docs/implementation-plan.md) — deploy messaging and Docker socket options.
