FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS base
WORKDIR /app
COPY pyproject.toml ./
RUN uv sync
COPY ./src /app/src

FROM base AS server
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS migrations
COPY alembic.ini ./alembic.ini
ENTRYPOINT ["uv", "run", "alembic"]