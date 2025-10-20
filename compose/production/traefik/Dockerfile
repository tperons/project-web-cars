# Usa a imagem oficial do Traefik com uma versão fixada para builds reprodutíveis.
FROM docker.io/traefik:3.5.3

# Prepara o diretório e o arquivo para armazenamento dos certificados SSL do Let's Encrypt.
RUN mkdir -p /etc/traefik/acme \
  # Cria o arquivo JSON onde os certificados serão salvos.
  && touch /etc/traefik/acme/acme.json \
  # Define permissões restritas (leitura/escrita apenas para o dono) no arquivo de certificados.
  # Esta é uma etapa de segurança CRUCIAL para proteger as chaves privadas.
  && chmod 600 /etc/traefik/acme/acme.json

# Copia o arquivo de configuração estática do Traefik para o diretório padrão do contêiner.
COPY ./compose/production/traefik/traefik.yml /etc/traefik