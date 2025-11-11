FROM python:3.14 AS base
WORKDIR /code
RUN pip install --no-cache-dir uv

COPY ./uv.lock /code/uv.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN uv sync 

FROM base AS base_with_code
COPY ./src ./src

FROM base AS dev
CMD ["uv", "run", "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

FROM base_with_code AS prod
EXPOSE 80
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]

FROM base_with_code AS migration
COPY ./alembic.ini /code/alembic.ini
CMD ["uv", "run", "alembic", "upgrade", "head"]