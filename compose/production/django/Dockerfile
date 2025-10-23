# Dockerfile para ambiente de produção (Multi-Stage)

# --- Estágio 1: Build Stage (A "Oficina") ---
# Começamos com a imagem oficial do Python e instalamos o 'uv'.
FROM python:3.14-slim-bookworm AS python-build-stage

RUN pip install uv

# Variáveis de ambiente para otimizar o 'uv'.
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# Define o diretório de trabalho.
ARG APP_HOME=/app
WORKDIR ${APP_HOME}

# Instala dependências de sistema necessárias APENAS para o build.
# 'build-essential' é pesado e só é necessário para compilar pacotes.
# Ele não estará na imagem final.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

# Instala as dependências de produção do Python em cache.
# '--no-dev' é CRUCIAL para não instalar pacotes de desenvolvimento.
# '--locked' garante que as versões do uv.lock sejam respeitadas.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copia o código da aplicação.
COPY . ${APP_HOME}

# Instala o projeto em si (sem dependências de dev).
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev

# --- Estágio 2: Run Stage (A Imagem Final) ---
# Começamos de uma imagem Python limpa e leve.
FROM python:3.14-slim-bookworm AS python-run-stage

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

# Cria um grupo e um usuário de sistema com privilégios limitados.
# Medida de segurança essencial para produção.
RUN addgroup --system django \
    && adduser --system --ingroup django django

# Instala APENAS as dependências de sistema necessárias para RODAR a aplicação.
# Note que 'build-essential' não está aqui.
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    wait-for-it \
    # Limpa o cache do apt para reduzir o tamanho da imagem.
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copia os scripts de inicialização e define o usuário 'django' como dono.
COPY --chown=django:django ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY --chown=django:django ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

# A mágica do multi-stage: copia a pasta /app (com código e venv) do estágio de build.
COPY --from=python-build-stage --chown=django:django ${APP_HOME} ${APP_HOME}

# Cria o diretório de mídia usando a variável PROJECT_NAME.
# Este diretório precisa pertencer ao usuário 'django' para uploads de arquivos.
RUN mkdir -p ${APP_HOME}/apps/media

# Garante que o usuário 'django' seja o dono de toda a pasta da aplicação.
RUN chown -R django:django ${APP_HOME}

# Adiciona os executáveis do ambiente virtual ao PATH.
ENV PATH="/app/.venv/bin:$PATH"

# Muda o usuário ativo para 'django'.
# Todos os comandos seguintes rodarão como este usuário.
USER django

# Compila os arquivos de tradução. As ENV vars são fakes para o manage.py rodar.
RUN DATABASE_URL="" \
    DJANGO_SETTINGS_MODULE="config.settings.test" \
    python manage.py compilemessages

# Ponto de entrada do contêiner.
ENTRYPOINT ["/entrypoint.sh"]