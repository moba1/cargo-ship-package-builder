FROM debian:latest

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
  && apt-get install -y \
    binutils bison diffutils flex gettext git \
    gawk m4 patch perl python3 texinfo build-essential \
    curl \
  && apt-get clean \
  && rm -Rf /var/lib/apt/lists/*

ENV WORK_ROOT /work
ENV APP_DIR /app
ENV DIST_DIR ${APP_DIR}/dist
WORKDIR ${APP_DIR}

# ENTRYPOINT ["./build.bash"]
