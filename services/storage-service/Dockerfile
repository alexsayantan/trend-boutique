# ==================== Builder Stage ====================
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

COPY services/storage-service/pyproject.toml ./services/storage-service/pyproject.toml

RUN uv venv
RUN uv pip install \
    boto3 \
    "grpcio>=1.80.0" \
    "grpcio-tools>=1.80.0" \
    "pydantic-settings>=2.13.1"

COPY services/storage-service ./services/storage-service

# ==================== Runtime Stage ====================

FROM python:3.14-slim-bookworm

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/services/storage-service /app/services/storage-service

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

RUN ln -s /app/services/storage-service /app/services/storage_service

CMD ["python", "services/storage-service/main.py"]
