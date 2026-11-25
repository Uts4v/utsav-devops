# ---- Stage 1: prepare static files ----
FROM alpine AS builder

WORKDIR /site
COPY . .

# ---- Stage 2: final nginx image ----
FROM nginx:alpine

COPY --from=builder /site /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80