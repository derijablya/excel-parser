FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.2

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

RUN apt-get update && apt-get install

RUN pip install --upgrade pip

RUN pip install poetry

COPY poetry.lock pyproject.toml /usr/src/app/

RUN poetry config virtualenvs.create false \
    && poetry install --only main

COPY . /usr/src/app/
