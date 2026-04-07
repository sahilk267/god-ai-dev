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
                            │ Output: URL      │
                            └──────────────────┘