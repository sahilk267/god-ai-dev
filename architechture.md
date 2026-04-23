# 🏗️ God-Level AI Developer System - Architecture

## 🎭 Multi-Agent Intelligence Layer

The system operates using a hierarchical multi-agent orchestration, supervised by the **Master Agent (Meta-Learner)**.

```mermaid
graph TD
    User((User)) -->|Prompt| Orchestrator[Orchestrator]
    
    subgraph "Meta-Learning Layer"
        Master[Master Agent] <--> Experience[(Experience DB)]
    end
    
    Orchestrator <-->|Consult Advice| Master
    
    subgraph "Execution Agents"
        Planner[Planner Agent]
        Architect[Architect Agent]
        Coder[Coder Agent]
        Tester[Tester Agent]
        Debugger[Debugger Agent]
        Reviewer[Reviewer Agent]
    end
    
    Orchestrator --> Planner
    Planner --> Architect
    Architect --> Coder
    Coder --> Reviewer
    Reviewer -->|Refinement Loop| Coder
    Coder --> Tester
    Tester -->|Error Logs| Debugger
    Debugger -->|Fixes| Coder
```

## 🧠 Key Components

### 1. Master Agent (The Brain)
- **Role**: Learns from historical data and external logs.
- **Function**: Distills patterns from chat history and build failures.
- **Memory**: Persistent Vector Store (ChromaDB) for long-term lesson retention.

### 2. Execution Agents
- **Planner**: Breaks down complex requests into actionable steps.
- **Architect**: Designs the system folder structure and defines file roles.
- **Coder**: Generates production-ready code emphasizing safety and logic.
- **Tester**: Automatically writes and executes Pytest/Unit tests.
- **Debugger**: Performs project-wide trace analysis and multi-file fixes.
- **Reviewer**: Audits code quality and security, triggering the Reflection Loop.

### 3. Experience Flow
1. **Importing**: User imports chat logs (from Cursor/GPT) or URLs.
2. **Extraction**: Master Agent uses LLM to identify coding preferences.
3. **Storage**: Patterns are indexed in Experience DB.
4. **Retrieval**: Orchestrator queries DB for advice before every new task.
5. **Continuous Learning**: Failed builds are analyzed by the Master Agent to prevent future repeating of mistakes.

## 🧠 Intelligence Stack

The system is optimized for high-performance open-source models:
- **Primary Model (Planning/Logic)**: `qwen2.5-coder:7b`
- **Coder Model (Development)**: `deepseek-coder:6.7b`
- **Maintenance Model (Fixes/Scraping)**: `deepseek-coder:1.3b`

## Project identity and workspace

- **`project_id`**: UUID returned by `POST /api/build` and used for `/api/status/...`, `/ws/...`, and listing in `/api/projects`.
- **`project_name`**: Directory name under `workspace/` where the coder writes files (from architect output). It is **not** the same as `project_id` until explicitly linked in application state (see [`docs/implementation-plan.md`](docs/implementation-plan.md) Phases 1–2).

## Documentation map (single source per topic)

| Topic | File |
|--------|------|
| Agent flow (ASCII) | [`agent diagram.md`](agent%20diagram.md) |
| HTTP / WebSocket API | [`api architechture.md`](api%20architechture.md) |
| Request pipeline | [`data flow.md`](data%20flow.md) |
| Redis, disk, GitHub, memory | [`db storage architechture.md`](db%20storage%20architechture.md) |
| Dev / prod Docker | [`deployment architechture.md`](deployment%20architechture.md) |
| Repo tree | [`structure.md`](structure.md) |
| Pipeline & IDE checklist | [`docs/implementation-plan.md`](docs/implementation-plan.md) |

Avoid duplicating full endpoint lists here; use **api architechture** as the canonical API reference.
