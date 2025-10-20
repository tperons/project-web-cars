# Usa a imagem oficial do PostgreSQL versão 17 como base.
# É uma boa prática fixar a versão para garantir builds consistentes.
FROM docker.io/postgres:17

# Copia a pasta local 'maintenance' (que contém scripts de backup, restore, etc.)
# para uma pasta temporária dentro do contêiner.
COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance

# Concede permissão de execução para todos os scripts na pasta 'maintenance'.
RUN chmod +x /usr/local/bin/maintenance/*

# Move os scripts para o diretório /usr/local/bin (que está no PATH do sistema)
# para que possam ser chamados globalmente, e em seguida remove a pasta temporária.
# Fazer isso em uma única camada RUN é uma prática de otimização.
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance