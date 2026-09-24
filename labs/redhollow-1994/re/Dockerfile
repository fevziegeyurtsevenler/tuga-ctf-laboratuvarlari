FROM debian:bookworm-slim AS build
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*
COPY src/bone_tagger.c /tmp/bone_tagger.c
RUN gcc -O1 -s -o /bone_tagger /tmp/bone_tagger.c

FROM debian:bookworm-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends binutils file xxd \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /bone_tagger /challenge/bone_tagger
WORKDIR /challenge
CMD ["bash", "-lc", "echo; echo 'Night Hatch analiz'; echo 'Program: ./bone_tagger'; echo; exec bash"]
