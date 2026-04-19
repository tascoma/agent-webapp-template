# CLAUDE.md

Practice project for building a server-rendered web app with an AI agent backend.

## Behavior

- **Simplicity first.** Prefer the smallest solution that works. No premature abstractions, no speculative flexibility, no helpers that wrap a one-liner.
- **Test after implementation.** After any code change, run the relevant tests (or write one if none exists for the path) before reporting the task complete.
- **Follow best practices.** Idiomatic FastAPI, Pydantic v2 syntax, modern SQLAlchemy 2.0 style, PEP 8 naming. If unsure, match the convention already in the codebase.
- **Type hints everywhere.** Every function signature and Pydantic field is typed. `mypy`/`pyright` should pass.
- **Async by default for routes.** FastAPI endpoints are `async def` unless they call blocking code that can't be made async.
- **Separate models and schemas.** SQLAlchemy ORM classes go in `models/`; Pydantic classes go in `schemas/`. Never merge them.
- **Dependency injection via `Depends()`.** DB sessions, settings, agents, and auth all flow through FastAPI dependencies — no module-level singletons passed around.
- **Log, don't print.** Use `logging.getLogger(__name__)`. `print()` is for scratch only and must not land in committed code.
- **Config comes from env.** All environment-dependent values go through `app.core.config.settings` — no hardcoded URLs, keys, or paths.
- **Validate at boundaries.** Pydantic handles input validation at the route layer; internal functions trust their callers and don't re-validate.
- **Ask before adding dependencies.** Check if the stdlib or existing deps already solve it before adding to `pyproject.toml`. Use `uv add <pkg>` (not `pip install`) so the lockfile stays in sync.
- **Small, focused changes.** One concern per commit. Don't bundle refactors with feature work.
- **No comments for what the code says.** Only comment the *why* when it's non-obvious (a workaround, a constraint, a subtle invariant).
- **Never commit secrets.** `.env` stays gitignored; `.env.example` documents the shape.

## Tech stack

- **FastAPI** — web framework, async routes, dependency injection
- **Pydantic v2** — request/response schemas and settings management (`BaseSettings`)
- **Pydantic-AI** — agent framework for structured LLM interactions
- **Jinja2** — server-side HTML templating (via `fastapi.templating.Jinja2Templates`)
- **SQLAlchemy** — ORM for persistence (engine/session wired in `app/database.py`)
- **Python stdlib `logging`** — configured in `app/core/logging.py`
- **uv** — package/dependency manager and virtual environment tool (replaces pip + venv)

## Project scaffold

```
fastapi-pydantic-ai-jinja2-practice/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance, router includes, lifespan
│   ├── database.py          # SQLAlchemy engine + session factory
│   ├── deps.py              # Shared Depends() factories (db session, current user, agents)
│   ├── core/                # Cross-cutting infrastructure
│   │   ├── config.py        # Pydantic BaseSettings (env-driven)
│   │   └── logging.py       # configure_logging() called on startup
│   ├── routes/              # APIRouter modules (one per resource/feature)
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── agents/              # Pydantic-AI agent definitions and tools
│   ├── services/            # Business logic between routes and models/agents
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, JS, images served at /static
├── tests/                   # pytest suite
├── logs/                    # Runtime log output (gitignored)
└── uploads/                 # User-uploaded files (gitignored)
```

## Conventions

- `models/` holds SQLAlchemy classes; `schemas/` holds Pydantic classes — keep them separate.
- Settings are accessed via a single `settings` instance imported from `app.core.config`.
- Logging is configured once at app startup; modules call `logging.getLogger(__name__)`.
- Templates and static assets live inside `app/` so they ship with the package.
- `logs/` is an output directory, not config — logging config lives in `app/core/logging.py`.
