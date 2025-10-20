#!/bin/bash

# Configura o "Modo Estrito" do Bash para um scripting mais seguro.
# Se qualquer comando falhar, o script irá parar imediatamente.
set -o errexit
set -o pipefail
set -o nounset

# --- Bloco de Configuração do Banco de Dados ---

# Verifica se a variável de ambiente POSTGRES_USER foi definida.
# Se não foi, assume o valor 'postgres', que é o usuário padrão
# da imagem oficial do PostgreSQL. Isso adiciona robustez à configuração.
if [ -z "${POSTGRES_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER="${base_postgres_image_default_user}"
fi

# Constrói a string de conexão DATABASE_URL a partir de outras variáveis de ambiente.
# Isso centraliza a configuração do banco em um formato que o Django (via dj-database-url) pode usar.
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"


# --- Bloco de Espera pelo Banco de Dados ---

# Usa o script 'wait-for-it' para pausar a execução até que o banco de dados esteja
# realmente pronto para aceitar conexões.
# Isso é VITAL em ambientes containerizados, onde a aplicação pode iniciar antes do banco.
# O timeout é de 30 segundos.
wait-for-it "${POSTGRES_HOST}:${POSTGRES_PORT}" -t 30

# Imprime uma mensagem no 'standard error' para o log, confirmando que o banco está acessível.
>&2 echo 'PostgreSQL is available'


# --- Bloco de Execução do Comando Principal ---

# 'exec "$@"' é um padrão crucial em entrypoints.
# Ele substitui o processo atual (o próprio script entrypoint)
# pelo comando que foi passado como argumento para ele (ex: o script '/start').
# Isso garante que o processo da aplicação seja o processo principal (PID 1)
# e receba os sinais do Docker corretamente (ex: para um desligamento limpo).
exec "$@"