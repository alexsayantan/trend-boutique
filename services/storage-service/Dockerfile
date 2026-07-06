# ==================== Builder Stage ====================
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_HTTP_TIMEOUT=120
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY services/*/pyproject.toml ./services/

RUN uv sync --frozen --no-dev --no-install-workspace

COPY . .

RUN uv sync --package storage-service --frozen --no-dev

# ==================== Runtime Stage ====================

FROM python:3.14-slim-bookworm

WORKDIR /app

COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

RUN ln -s /app/services/storage-service /app/services/storage_service

CMD ["python", "services/storage-service/main.py"]