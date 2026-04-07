┌─────────────────────────────────────────────────────────────────────────────┐
│                              API LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  METHOD   ENDPOINT              DESCRIPTION           AUTH                   │
│  ─────────────────────────────────────────────────────────────────────────  │
│  POST     /api/build            Start new project     Optional              │
│  GET      /api/status/{id}      Get project status    Optional              │
│  GET      /api/projects         List all projects     Optional              │
│  DELETE   /api/projects/{id}    Cancel project        Optional              │
│  GET      /api/health           Health check          None                  │
│  GET      /api/metrics          Prometheus metrics    Internal              │
│  WS       /ws/{id}              Live logs stream      Optional              │
│  GET      /                     Serve frontend        None                  │
│  GET      /editor               Monaco editor         None                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘