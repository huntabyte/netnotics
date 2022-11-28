FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/opt/venv

ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"


RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # deps for installing poetry
    curl \
    # deps for building python deps
    build-essential \
    \
    # install poetry - uses $POETRY_VERSION internally
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && mv /root/.poetry $POETRY_PATH \
    && poetry --version \
    \
    # configure poetry & make a virtualenv ahead of time since we only need one
    && python -m venv $VENV_PATH \
    && poetry config virtualenvs.create false \
    \
    # cleanup
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y curl
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-ansi -vvv
COPY . ./

CMD poetry run uvicorn app.main:app --host 0.0.0.0
