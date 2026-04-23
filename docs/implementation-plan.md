# Implementation plan — pipeline fixes & IDE readiness

This plan follows the analysis of download/deploy/test/debug behavior and prepares a path toward Cursor/VS Code integration. Work in **phase order**; verify acceptance criteria before starting the next phase.

**How to use:** Check items as you complete them (`[ ]` → `[x]`). Mark a **phase** done only when all its **tasks** and **acceptance** boxes for that phase are checked.

---

## Overall progress (mark phase done when all checklists below are complete)

- [ ] **Preconditions** (three items in next section)
- [ ] **Phase 1** — Canonical project metadata
- [ ] **Phase 2** — Download API
- [ ] **Phase 3** — Deploy messaging
- [ ] **Phase 4** — DevOps expectations
- [ ] **Phase 5** — Test / debugger quality
- [ ] **Phase 6** — IDE integration

**Optional gates:**

- [ ] Phase 1 done before starting Phase 2
- [ ] Phase 2 smoke-tested (download ZIP) before closing the “download bug” thread
- [ ] Phase 3 done — no `Project ready! None` in full build logs
- [ ] Phases 1–3 done before Phase 6 (docs/UI)

---

## Preconditions (verify once)

Check when verified:

- [ ] **Disk layout:** After a successful build, `workspace/` contains a folder named **`project_name`** (from architect/coder), not the task UUID.
- [ ] **API identity:** `GET /api/projects` returns **UUID** keys from `orchestrator.active_projects`.
- [ ] **Deploy in Docker:** Confirmed backend logs show **Docker not available** unless Docker socket is mounted; expect `url: null` unless GitHub succeeds.

| Check | How to verify |
|--------|----------------|
| Disk layout | After a successful build, `workspace/` contains a folder named **`project_name`** (from architect/coder), not the task UUID. |
| API identity | `GET /api/projects` returns **UUID** keys from `orchestrator.active_projects`. |
| Deploy in Docker | Backend logs show **Docker not available** unless the Docker socket is mounted — expect `url: null` unless GitHub succeeds. |

---

## Phase 1 — Canonical project metadata (foundation)

**Goal:** One source of truth linking **task UUID** → **on-disk folder** (`project_name`) and optional paths.

**Dependencies:** None.

### Tasks

- [ ] Extend `orchestrator.active_projects[project_id]` when the pipeline knows the folder name (at minimum after `build_code` returns), e.g. `project_name: str` and optional `workspace_subdir: str`.
- [ ] On task **start**, keep existing fields (`status`, `logs`); set `project_name` to `null` / omit until coding step completes.
- [ ] Ensure **failure/cancel** paths do not leave misleading `project_name` (set only when `create_project_structure` succeeds, or clear on failure — per your chosen rule).

### Acceptance criteria

- [ ] For any `project_id` in `active_projects` with status `completed` or `failed` **after coding**, `project_name` is present if files were written under `workspace/<project_name>/`.
- [ ] No breaking change to WebSocket or `/api/status/{id}` consumers (**additive** fields only).

### Phase 1 — Definition of done

- [ ] Code reviewed / merged
- [ ] Manual smoke: start build → inspect `GET /api/status/{uuid}` includes `project_name` when expected

---

## Phase 2 — Download API (UUID → disk folder)

**Goal:** `GET /api/projects/{project_id}/download` zips the **actual artifact directory**.

**Dependencies:** Phase 1.

### Tasks

- [ ] In `download_project` route: resolve folder using `active_projects[project_id].get("project_name")` (or stored `workspace_subdir`).
- [ ] If `project_name` missing: fall back to `_safe_path(project_id)` **only if** that path exists (legacy layout).
- [ ] If resolved path missing or empty: **404** with clear detail, e.g. `Project not found or no files yet` (distinct from traversal errors).
- [ ] Decide and document zip filename: `{project_id}.zip` vs `{project_name}.zip` (document in this file or README).

### Acceptance criteria

- [ ] After a completed build, download returns **200** + zip with generated files.
- [ ] No false **404** when artifacts exist under `workspace/<project_name>/`.
- [ ] `_safe_path` still blocks path traversal.

### Phase 2 — Definition of done

- [ ] `curl`/browser download tested with a fresh build
- [ ] Zip contents match `workspace/<project_name>/`

---

## Phase 3 — Deploy messaging and honest status

**Goal:** Logs and API never show literal **`None`** when deploy has no URL; status reflects reality.

**Dependencies:** None (can parallelize with Phase 1); ideally before Phase 4 UX.

### Tasks

- [ ] Orchestrator final log: use `deployment.get("url") or "<fallback message>"` (not `.get("url", default)` when value can be `None`).
- [ ] (Optional) Add `deployment_summary` / expose `docker`, `github`, `url` on status or task result for UI badges.
- [ ] README: document in-container deploy (Docker socket + engine) vs **GitHub** for a remote URL.

### Acceptance criteria

- [ ] Completed build log **never** contains `Project ready! None`.
- [ ] `deployment` remains JSON-serializable; frontend can use `url` truthiness.

### Phase 3 — Definition of done

- [ ] One full build observed in UI/logs with correct fallback text when `url` is null

---

## Phase 4 — DevOps expectations (Docker / GitHub)

**Goal:** Align product behavior with environment capabilities.

**Dependencies:** Phase 3 for messaging; infra changes can be parallel.

### Tasks (pick what matches your product)

- [ ] **A.** Docker Compose: optional `docker.sock` mount + env for engine; document security/port-mapping risks — **or** explicitly deferred.
- [ ] **B.** Treat “deploy” as **artifact ready** when Docker unavailable: human-readable message; no implied URL — **or** explicitly deferred.
- [ ] **C.** GitHub: `.env` token documented; failures surfaced clearly (log or API) — **or** explicitly N/A.

### Acceptance criteria

- [ ] No silent `url: null` without operator-visible explanation (log and/or API).
- [ ] If Docker intentionally off: no repeated error spam (single log, debug, or documented ignore).

### Phase 4 — Definition of done

- [ ] Decision recorded (which of A/B/C shipped vs deferred)
- [ ] README or runbook updated

---

## Phase 5 — Test / debugger loop quality

**Goal:** Reduce repeated “Debugger fallback” with no real change.

**Dependencies:** None; can run after Phase 2.

### Tasks

- [ ] Improve debugger prompt / response format (JSON schema or fenced JSON); **one** retry on parse failure before fallback.
- [ ] Fallback: do not re-write identical file content (hash or compare); log **why** JSON failed.
- [ ] Pass trimmed **pytest stdout/stderr** into `fix_errors` for targeted fixes.
- [ ] (Optional) After N identical failures: skip tests with user-visible warning — **or** explicitly deferred.

### Acceptance criteria

- [ ] Failure runs show **actionable** debugger output, not three identical meaningless “fallback” lines for one root cause.
- [ ] Tests still use async subprocess (no event-loop regression).

### Phase 5 — Definition of done

- [ ] At least one failing-test scenario exercised; logs reviewed
- [ ] (If added) unit/integration test for debugger JSON path

---

## Phase 6 — IDE integration (Cursor / VS Code) — incremental

**Goal:** Users can open generated code without a custom extension first.

**Dependencies:** Phase 1–2 strongly recommended first.

### Tasks

- [ ] Document host path `./workspace/<project_name>` (bind mount) in README or `docs/`.
- [ ] UI or README: **“Open in editor”** hint — path copy and/or optional `vscode://` / `cursor://` (note OS limits).
- [ ] (Later / optional) `GET /api/projects/{id}/metadata` → `{ project_id, project_name, relative_path }`.
- [ ] (Later / optional) VS Code/Cursor task or extension calling `/api/build` + `/api/status/{id}`.

### Acceptance criteria

- [ ] Developer can locate generated code on disk in **one** documented step after Phase 1–2.
- [ ] Phase 6 optional items clearly marked as future work if not done.

### Phase 6 — Definition of done

- [ ] Doc reviewed by someone who did not write the feature
- [ ] (If UI hint) visible on main flow or linked from README

---

## Suggested execution order

1. Phase 1 → Phase 2 (fixes download and ID confusion).
2. Phase 3 (quick win, fixes “None” in UI).
3. Phase 4 (environment/product alignment).
4. Phase 5 (debugger/tests — larger surface).
5. Phase 6 (docs + optional deep integration).

---

## Risks and notes

- **In-memory `active_projects`:** After backend restart, UUID → `project_name` mapping is lost; download may 404 until you add **persistence** (Redis/DB) or **scan workspace** by convention — note as future work if needed.
- **Multi-tenant / security:** Any new metadata endpoint must not leak other users’ paths if you add auth later.

---

## Traceability to original issues

| Symptom | Addressed by |
|---------|----------------|
| Download 404 / “Project empty” | Phase 1 + 2 |
| “Project ready! None” | Phase 3 |
| Docker URL missing | Phase 3 + 4 |
| Repeated test / debugger fallback | Phase 5 |
| Cursor/VS Code workflow | Phase 6 |

---

## Related documentation (aligned with this plan)

Single-topic sources — avoid duplicating long API tables in multiple files:

| Topic | File |
|--------|------|
| REST / WebSocket reference | [api architechture.md](../api%20architechture.md) |
| Mermaid + doc map | [architechture.md](../architechture.md) |
| Agent ASCII diagram | [agent diagram.md](../agent%20diagram.md) |
| Request pipeline | [data flow.md](../data%20flow.md) |
| Storage (Redis, disk, GitHub, Chroma) | [db storage architechture.md](../db%20storage%20architechture.md) |
| Docker dev / prod | [deployment architechture.md](../deployment%20architechture.md) |
| Repo tree | [structure.md](../structure.md) |
| Quick start + links | [README.md](../README.md) |
