# Storage architecture

Where state and artifacts live. Implementation checklist: [`docs/implementation-plan.md`](docs/implementation-plan.md).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           STORAGE LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐       │
│  │     REDIS        │     │   FILE SYSTEM    │     │     GITHUB       │       │
│  │                  │     │                  │     │                  │       │
│  │ • Configured via │     │ • Source code    │     │ • Remote repo    │       │
│  │   REDIS_URL      │     │   workspace/     │     │ • Push from      │       │
│  │ • Ready for      │     │ • Logs logs/     │     │   devops agent   │       │
│  │   future queue / │     │ • ChromaDB data  │     │                  │       │
│  │   cache use      │     │   workspace/     │     │                  │       │
│  │                  │     │   .memory/       │     │                  │       │
│  └──────────────────┘     └──────────────────┘     └──────────────────┘       │
│                                                                              │
│  Redis default: :6379     Workspace: ./workspace/      GitHub: HTTPS API     │
│  Task queue today: in-process asyncio (see data flow.md)                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## In-memory (runtime)

- **`orchestrator.active_projects`**: status and logs per `project_id` (UUID). Lost on process restart — see risks in [`docs/implementation-plan.md`](docs/implementation-plan.md).
- **`task_queue.tasks`**: task metadata and asyncio queue (not persisted to Redis yet).

## ChromaDB (experience)

- Path: **`workspace/.memory/`** (persistent embeddings / collections for Master Agent).
