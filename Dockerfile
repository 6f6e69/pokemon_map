FROM python:3.11-slim AS builder

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /venv

COPY poetry.lock pyproject.toml ./

ARG dev

RUN if [ -z "${dev}"] ; \
    then \
        poetry install --no-root --no-ansi --without dev ; \
    else \
        poetry install --no-root --no-ansi --with dev ; \
    fi

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/venv/.venv/bin:$PATH"

COPY --from=builder /venv/.venv /venv/.venv

WORKDIR /app
