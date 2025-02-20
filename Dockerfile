FROM python:3.12-alpine

ENV POETRY_VERSION=2.1.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

    RUN apk add --no-cache \
    curl \
    bash \
    git \
    build-base \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
COPY oauth_shield ./oauth_shield
COPY templates ./templates
COPY site ./site

RUN if [ -f pyproject.toml ]; then poetry install; fi

EXPOSE 8000

CMD ["poetry", "run", "fastapi", "run", "/app/oauth_shield/main.py"]
