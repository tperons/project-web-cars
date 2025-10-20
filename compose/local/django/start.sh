#!/bin/bash

# Configura o "Modo Estrito" do Bash para um scripting mais seguro.
# -o errexit: Sai imediatamente se um comando falhar.
# -o pipefail: O status de saída de um pipeline é o do último comando a falhar.
# -o nounset: Trata variáveis não definidas como um erro.
set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate

# Inicia o servidor de desenvolvimento do Django.
# 'exec' é crucial: ele substitui o processo do script pelo do Django,
# permitindo que o contêiner gerencie o processo do servidor diretamente (ex: para desligamentos limpos).
# 'runserver_plus' é uma versão melhorada do runserver padrão (do django-extensions).
# '0.0.0.0:8000' é necessário para que a aplicação seja acessível de fora do contêiner.
exec python manage.py runserver_plus 0.0.0.0:8000