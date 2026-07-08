FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY shared/pyproject.toml ./shared/
COPY services/cart-service/pyproject.toml ./services/cart-service/
RUN uv sync --frozen --no-dev --no-install-workspace
COPY . .
RUN uv sync --package cart-service --frozen --no-dev

FROM python:3.14-slim-bookworm
WORKDIR /app
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
CMD ["fastapi", "run", "services/cart-service/main.py", "--host", "0.0.0.0", "--port", "8000"]
