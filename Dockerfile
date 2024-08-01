ARG FUNCTION_DIR="/workspace/code"

FROM python:3.11

ARG FUNCTION_DIR

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH "/root/.local/bin:$PATH"

RUN poetry config virtualenvs.in-project true

ENV PATH "${FUNCTION_DIR}/.venv/bin:$PATH"

COPY pyproject.toml poetry.lock $FUNCTION_DIR

RUN poetry install --no-interaction --no-root

COPY storagesbug/ ${FUNCTION_DIR}

ENTRYPOINT ["python", "manage.py", "collectstatic" ,"--noinput"]
