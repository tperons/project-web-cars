# Usa a imagem oficial do Nginx com a tag 'alpine'.
# 'alpine' cria uma imagem final muito menor, o que é ideal para produção.
# A versão (1.29.1) é fixada para garantir builds reprodutíveis.
FROM docker.io/nginx:1.29.1-alpine

# Copia o arquivo de configuração customizado do Nginx do nosso projeto
# para o diretório padrão de configurações dentro do contêiner.
# O Nginx irá carregar este arquivo automaticamente ao iniciar.
COPY ./compose/production/nginx/default.conf /etc/nginx/conf.d/default.conf