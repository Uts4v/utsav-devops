# ---- Stage 1: prepare static files ----
FROM alpine AS builder

WORKDIR /site
COPY . .

# ---- Stage 2: final nginx image ----
FROM nginx:alpine

RUN chown -R nginx:nginx /var/cache/nginx /usr/share/nginx/html \
    && touch /var/run/nginx.pid \
    && chown nginx:nginx /var/run/nginx.pid

COPY --chown=nginx:nginx --from=builder /site /usr/share/nginx/html
COPY --chown=nginx:nginx nginx.conf /etc/nginx/conf.d/default.conf

USER nginx

EXPOSE 8080
