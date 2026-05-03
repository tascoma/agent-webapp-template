# Agent Webapp Template

A template for building React + FastAPI web applications with a [Pydantic AI](https://ai.pydantic.dev/) agent backend.

## Stack

- **React + Vite** — frontend UI
- **FastAPI** — async web framework with dependency injection
- **Pydantic AI** — structured LLM agent framework
- **Pydantic v2** — request/response schemas and settings via `BaseSettings`
- **SQLAlchemy 2.0** — async ORM
- **uv** — dependency and virtual environment management

## Getting started

### 1. Clone and install dependencies

```bash
git clone https://github.com/tascoma/agent-webapp-template.git
cd agent-webapp-template
uv sync
```

### 2. Configure environment

```bash
cp .env.example .env
```

Fill in the values in `.env`:

```env
APP_ENV=development
SECRET_KEY=              # openssl rand -hex 32
DATABASE_URL=sqlite+aiosqlite:///./app.db
ANTHROPIC_API_KEY=       # from console.anthropic.com
```

### 3. Run the backend

```bash
cd backend
uv run python -m app.main
```

### 4. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

## Project structure

```
agent-webapp-template/
├── .env.example
├── pyproject.toml
├── frontend/                # React + Vite app
└── backend/
    ├── app/
    │   ├── main.py          # FastAPI app, CORS, lifespan
    │   ├── core/
    │   │   ├── config.py    # Pydantic BaseSettings (env-driven)
    │   │   └── logging.py   # Rotating file + console logging
    │   ├── agents/          # Pydantic AI agent definitions and tools
    │   ├── dependencies/    # Shared Depends() factories
    │   ├── databases/       # SQLAlchemy engine and session factory
    │   ├── routes/          # APIRouter modules (one per resource)
    │   ├── models/          # SQLAlchemy ORM models
    │   ├── schemas/         # Pydantic request/response schemas
    │   └── services/        # Business logic layer
    ├── tests/
    ├── logs/
    └── uploads/
```

## Using this template

See [CLAUDE.md](CLAUDE.md) for step-by-step wiring instructions covering each layer of the stack.
