# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY backend/app ./backend/app

RUN uv sync --no-dev

WORKDIR /app/backend

EXPOSE 8000

CMD uv run python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
