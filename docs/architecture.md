# Architecture

This repo is a template for full-stack apps with an LLM agent backend: a
**FastAPI** service exposing a **Pydantic-AI** agent, a **React + Vite**
frontend, and an optional **Swift/SwiftUI** iOS app, all backed by an
optional **Supabase** Postgres database. It ships as a deliberately thin
scaffold — most layers exist as empty, conventionally-named directories that
get filled in by running a Claude Code skill (see [Extending this
template](#extending-this-template)) rather than by hand-rolling boilerplate
each time.

## Tech stack

| Layer | Choice |
|---|---|
| Backend framework | FastAPI (async, dependency-injection-first) |
| Agent framework | [Pydantic-AI](https://ai.pydantic.dev/), model `anthropic:claude-sonnet-4-6` |
| Validation / settings | Pydantic v2 (`pydantic-settings` for config) |
| Database | Supabase Postgres (optional), SQLAlchemy 2.0 async ORM (added on demand) |
| Migrations | Alembic (added on demand) |
| File storage | Supabase Storage (optional) |
| Web frontend | React + Vite + TypeScript |
| iOS | Swift / SwiftUI |
| Hosting | Render (backend as Web Service, frontend as Static Site) |
| Tooling | `uv` for Python deps/venv, Python ≥ 3.12 |

## Repository layout

```
agent-webapp-template/
├── backend/
│   └── app/
│       ├── main.py          # FastAPI app, CORS, lifespan, /api/health
│       ├── core/             # config.py (settings), logging.py
│       ├── agents/           # Pydantic-AI agent definitions
│       ├── dependencies/     # Depends() factories (get_agent, get_storage_client)
│       ├── databases/        # empty — async engine/session/Base (via /setup)
│       ├── routes/           # empty — APIRouter modules (via /add-resource)
│       ├── models/           # empty — SQLAlchemy ORM models (via /add-resource)
│       ├── schemas/          # empty — Pydantic request/response schemas
│       └── services/         # storage.py; business logic lives here
├── frontend/                 # React + Vite app
├── ios/                      # Swift iOS app (created via /setup-ios)
└── skills/                   # Claude Code task playbooks, one dir per skill
```

`databases/`, `routes/`, `models/`, and `schemas/` exist as placeholders —
they're the conventional homes for code that skills generate, not dead code
to delete.

## Backend architecture

`main.py` wires up the FastAPI app: a `lifespan` hook calls
`configure_logging()` on startup, CORS middleware reads allowed origins from
settings, and `/api/health` is the only route mounted out of the box.
Routers are added with a one-liner as resources are created:

```python
# from app.routes import items
# app.include_router(items.router, prefix="/api/items", tags=["items"])
```

The intended request flow once resources exist is:

```
routes/ (APIRouter, HTTP concerns)
  → services/ (business logic)
    → models/ (SQLAlchemy ORM) + schemas/ (Pydantic I/O contracts)
```

Dependencies are centralized in `dependencies/__init__.py` as small factory
functions passed to `Depends(...)`, e.g. `get_agent()` returns the shared
agent instance, and `get_storage_client()` builds a Supabase client (raising
if Supabase env vars aren't set). New resources following `/add-resource`
add their own `get_*_service` factories alongside these.

**Config and logging** (`core/`): `config.py` defines a single
`pydantic-settings` `Settings` object loaded from `../.env`, covering app
env, secrets, host/port, CORS origins, the database URL, optional Supabase
credentials, and the Anthropic API key/model. `logging.py` configures a
root logger with a console handler and a rotating file handler
(`backend/logs/app.log`, 10 MB × 5 backups).

## Agent architecture

`agents/agent.py` defines one module-level Pydantic-AI `Agent`, configured
with the model id from settings and a system prompt. Tools are attached with
the `@agent.tool_plain` decorator — the template ships one example,
`get_current_time()`. `dependencies.get_agent()` returns this shared
instance so routes/services can depend on it instead of importing the
module-level singleton directly. Adding more agents (e.g. a separate agent
per domain, or one with richer tools/dependencies) is handled by
`/add-agent`, which follows this same module-plus-dependency-factory
pattern.

## Frontend architecture

The Vite dev server proxies `/api/*` to `http://localhost:8000`
(`vite.config.ts`), so the app talks to the backend without CORS
configuration in development. `src/lib/api.ts` is a minimal typed fetch
wrapper (`api.get/post/patch/delete`) that prefixes requests with `/api` and
reads `VITE_API_URL` as the base URL in production, where there's no dev
proxy. `App.tsx` currently just renders the result of `/api/health` to prove
the wiring works. Routing, global state, and auth context don't exist yet —
they're added by `/setup-frontend`, and individual pages/features by
`/add-frontend-feature`.

## Data layer

Supabase is optional and the app boots without it. Two independent pieces
plug in as needed:

- **Database**: `DATABASE_URL` is a required setting, but nothing reads it
  yet — `/setup-supabase` provisions a Supabase Postgres instance and
  `/setup` (or `/setup-supabase`) wires up the SQLAlchemy async engine and
  session factory in `databases/`. Schema changes go through Alembic, set
  up via `/add-migration` (currently `backend/alembic/` is an empty
  placeholder).
- **Storage**: `services/storage.py` has upload/delete helpers against
  Supabase Storage, and `get_storage_client()` raises a clear error if
  `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` aren't set. `/setup-storage`
  walks through configuring a bucket and these env vars.

## Auth

No authentication exists in the base template. `/add-auth` adds Supabase
Auth end-to-end: JWT verification and a `current_user` FastAPI dependency
on the backend, protected routes, and matching login/session flows in the
React frontend and iOS app.

## Deployment

`/setup-render` provisions the backend as a Render Web Service and the
frontend as a Render Static Site; `/setup-ci` adds GitHub Actions for CI and
auto-deploy on merge. Environments follow branch promotion:

| Branch | Environment | Database |
|---|---|---|
| `main` | Production | Supabase prod |
| `dev` | Staging | Supabase staging |
| `feature/*` | Local | Local or staging |

Feature branches are cut from `dev`, PR'd back to `dev`, then promoted to
`main` — never committed to directly (see `/github-workflow`).

## Extending this template

This template is meant to be grown with skills, not by copying code from
elsewhere in the repo. The skills table in [CLAUDE.md](../CLAUDE.md) is the
full reference; the common path from empty scaffold to working feature is:

- **New CRUD resource** → `/add-resource` (model, schema, dependency,
  service, router, tests)
- **New agent or tool** → `/add-agent`
- **Database** → `/setup-supabase` to provision it, then `/add-migration`
  for schema changes, `/seed-database` for reference data
- **Auth** → `/add-auth`
- **File uploads** → `/setup-storage`
- **Frontend** → `/setup-frontend` once, then `/add-frontend-feature` per
  page
- **Tests** → `/add-tests` (backend), `/test-frontend`, `/test-agent`
- **Ship it** → `/setup-render`, `/setup-ci`
