FROM traefik:v2.0-alpine
RUN mkdir -p /etc/traefik/acme
RUN touch /etc/traefik/acme/acme.json
RUN chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/local/traefik/traefik.toml /etc/traefik
COPY ./compose/local/traefik/dynamic-conf.toml /etc/traefik
