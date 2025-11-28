FROM python:3.13-slim-bookworm AS builder

RUN pip install uv

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --no-install-project

FROM python:3.13-slim-bookworm

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq5 \
    gettext \
    wait-for-it \
    sudo \
    git \
    bash-completion \
    nano \
    ssh \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv

RUN groupadd --gid 1000 dev-user \
    && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
    && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
    && chmod 0440 /etc/sudoers.d/dev-user

ENV PATH="/${APP_HOME}/.venv/bin:$PATH"
ENV PYTHONPATH="${APP_HOME}/.venv/lib/python3.13/site-packages:$PYTHONPATH"

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
COPY ./compose/local/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /entrypoint.sh /start.sh \
    && chmod +x /entrypoint.sh /start.sh

ENTRYPOINT ["/entrypoint.sh"]
