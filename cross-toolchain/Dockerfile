FROM debian:latest

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
  && apt-get install -y \
    binutils bison diffutils flex gettext git file \
    gawk m4 patch perl python3 texinfo build-essential \
    curl \
  && apt-get clean \
  && rm -Rf /var/lib/apt/lists/*

ARG ARCH
ARG TARGET
ARG WORK_ROOT
ENV APP_DIR=/app DIST_DIR=/var/tmp TOOL_DIR="${WORK_ROOT}/tools"
COPY ./src "${APP_DIR}"
RUN bash "${APP_DIR}/init.bash" \
  && bash "${APP_DIR}/main.bash" \
  && rm -Rf /var/tmp/* \
  && rm -Rf "${APP_DIR}"/*
