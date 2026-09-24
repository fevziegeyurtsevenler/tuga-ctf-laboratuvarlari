FROM debian:bookworm-slim AS tagger
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*
COPY re/src/bone_tagger.c /tmp/bone_tagger.c
RUN gcc -O1 -s -o /bone_tagger /tmp/bone_tagger.c

FROM nginx:alpine
RUN rm -f /etc/nginx/conf.d/default.conf
COPY nginx/game.conf /etc/nginx/conf.d/game.conf
COPY game /usr/share/nginx/html
COPY --from=tagger /bone_tagger /usr/share/nginx/html/downloads/bone_tagger
EXPOSE 80
