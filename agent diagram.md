# Agent diagram

```
                          ┌─────────────────┐
                          │   ORCHESTRATOR   │
                          │     (Master)     │
                          └────────┬────────┘
                                   │
        ┌──────────────┬───────────┼───────────┬──────────────┐
        │              │           │           │              │
        ▼              ▼           ▼           ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   PLANNER    │ │  ARCHITECT   │ │    CODER     │ │   TESTER     │ │  DEBUGGER    │
│              │ │              │ │              │ │              │ │              │
│ Input: task  │ │Input: steps  │ │Input: design │ │Input: code   │ │Input: error  │
│ Output:steps │ │Output:design │ │Output: files │ │Output: tests │ │Output: fixed │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
        │              │              │              │              │
        └──────────────┴──────────────┼──────────────┴──────────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │    REVIEWER      │
                            │                  │
                            │ Input: code      │
                            │ Output: score    │
                            │ + suggestions    │
                            └────────┬─────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │     DEVOPS       │
                            │                  │
                            │ Input: project   │
                            │ Output: URL*     │
                            └──────────────────┘
```

\* **URL** is set when Docker deploy or GitHub push succeeds; otherwise may be absent (`null`). See [`deployment architechture.md`](deployment%20architechture.md).

**Meta-learning (parallel to this pipeline):** **Master Agent** + **Experience (ChromaDB)** — orchestrator consults memory before planning and learns from failures. Diagram: [`architechture.md`](architechture.md) (mermaid).

**Project ids:** API and WebSocket use **task UUID** (`project_id`); generated files live under **`workspace/<project_name>/`**. Pipeline alignment: [`docs/implementation-plan.md`](docs/implementation-plan.md).
