FROM python:3.13-slim-bookworm AS python-build-stage

RUN pip install uv

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . ${APP_HOME}

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev

FROM python:3.13-slim-bookworm AS python-run-stage

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq5 \
    gettext \
    wget \
    && wget -O /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=django:django ./compose/production/django/entrypoint.sh /entrypoint.sh
COPY --chown=django:django ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /entrypoint.sh /start.sh \
    && chmod +x /entrypoint.sh /start.sh

COPY --from=python-build-stage --chown=django:django ${APP_HOME} ${APP_HOME}

RUN mkdir -p ${APP_HOME}/apps/media \
    && chown -R django:django ${APP_HOME}

ENV PATH="/app/.venv/bin:$PATH"

USER django

RUN DATABASE_URL="" \
    DJANGO_SETTINGS_MODULE="core.settings.test" \
    python manage.py compilemessages

ENTRYPOINT ["/entrypoint.sh"]
