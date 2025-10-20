#!/bin/bash

# Configura o "Modo Estrito" do Bash para um scripting mais seguro.
set -o errexit
set -o pipefail
set -o nounset


# --- Bloco de Preparação de Arquivos Estáticos ---

# Executa o comando 'collectstatic' do Django.
# Este comando reúne todos os arquivos estáticos (CSS, JS, imagens)
# de todas as apps em um único diretório (definido em STATIC_ROOT nas settings).
# Em produção, um servidor web como o Nginx será configurado para servir
# os arquivos diretamente desta pasta, o que é muito mais eficiente.
# A flag '--noinput' garante que o comando rode sem interação do usuário.
python /app/manage.py collectstatic --noinput


# --- Bloco de Inicialização do Servidor de Aplicação ---

WORKERS=${GUNICORN_WORKERS:-$((2 * $(nproc) + 1))}
export WORKERS

# Inicia o servidor de produção Gunicorn.
# 'exec' substitui o processo do script pelo do Gunicorn, tornando-o o processo
# principal do contêiner, o que é crucial para o gerenciamento do Docker.
# 'config.wsgi' é o ponto de entrada da aplicação Django.
# '--bind 0.0.0.0:5000' faz o servidor ser acessível de fora do contêiner.
# '--chdir=/app' define o diretório de trabalho para evitar problemas com caminhos.
exec gunicorn config.wsgi --bind 0.0.0.0:8000 --workers "$WORKERS" --chdir=/app