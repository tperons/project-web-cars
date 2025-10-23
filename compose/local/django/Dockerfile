# Dockerfile para ambiente de desenvolvimento local

# Estágio 1: Define a imagem base
# Usamos a imagem oficial do Python 3.14 na sua versão 'slim-bookworm'.
# 'slim' é menor que a padrão e 'bookworm' é a versão estável do Debian.
# O 'AS python' cria um alias para este estágio, que podemos reutilizar.
FROM python:3.14-slim-bookworm AS python

# Instala o 'uv' manualmente usando pip.
# Este comando adiciona o 'uv' à nossa imagem base para que possamos usá-lo depois.
RUN pip install uv

# Estágio 2: Build da aplicação
# Começamos a partir da imagem base que preparamos no estágio anterior.
FROM python AS python-build-stage

# Define uma variável de ambiente para o diretório da aplicação. Facilita a manutenção.
ARG APP_HOME=/app

# Define o diretório de trabalho padrão dentro do contêiner.
WORKDIR ${APP_HOME}

# Variáveis de ambiente para otimizar o 'uv'.
# UV_COMPILE_BYTECODE=1: Gera arquivos .pyc, o que pode acelerar a inicialização da aplicação.
# UV_LINK_MODE=copy: Usa cópia em vez de links simbólicos, mais robusto no Docker.
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# Instala dependências a nível de sistema operacional (pacotes Debian).
RUN apt-get update && apt-get install --no-install-recommends -y \
    # Essencial para compilar pacotes Python que usam código C (ex: numpy, Pillow).
    build-essential \
    # Dependências para o 'psycopg', o driver do PostgreSQL para Python.
    # Se não for usar Postgres, pode remover.
    libpq-dev \
    # Ferramenta para internacionalização (traduções) no Django.
    gettext \
    # Script que espera um serviço (ex: banco de dados) ficar disponível antes de continuar.
    wait-for-it

# Instala as dependências Python usando um cache para acelerar builds futuros.
# Esta é a parte mais eficiente: montamos apenas os arquivos de dependência,
# sem copiar o projeto inteiro. O uv instala tudo que está no uv.lock.
# O '--no-install-project' instala apenas as dependências, não o projeto em si (que ainda não foi copiado).
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock:rw \
    uv sync --no-install-project

# Agora, copia todo o código do projeto para o diretório de trabalho no contêiner.
COPY . ${APP_HOME}

# Instala o projeto em si (e verifica novamente as dependências).
# Como as dependências já estão em cache da etapa anterior, isso é muito rápido.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock:rw \
    uv sync

# Configura o PATH para que os executáveis do ambiente virtual (como 'django-admin')
# sejam encontrados automaticamente no terminal do contêiner.
ENV PATH="/${APP_HOME}/.venv/bin:$PATH"

# Copia o script de entrypoint. Ele geralmente contém lógicas como
# aplicar migrações ou esperar o banco de dados ficar online.
COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
# Corrige possíveis problemas de quebra de linha (Windows CRLF vs Linux LF).
RUN sed -i 's/\r$//g' /entrypoint.sh
# Torna o script executável.
RUN chmod +x /entrypoint.sh

# Copia o script de start, que é o comando que efetivamente inicia o servidor de desenvolvimento.
COPY ./compose/local/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

# Define o comando padrão que será executado quando o contêiner iniciar.
# Ele chama o script 'entrypoint', que por sua vez geralmente chama o script 'start'.
ENTRYPOINT ["/entrypoint.sh"]