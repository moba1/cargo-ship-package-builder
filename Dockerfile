FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
RUN sed -i -r 's!(deb|deb-src) \S+!\1 mirror://mirrors.ubuntu.com/mirrors.txt!' /etc/apt/sources.list \
  && apt-get update \
  && apt-get install -y software-properties-common \
  && apt-add-repository --yes --update ppa:ansible/ansible \
  && apt-get install -y \
    ansible binutils bison diffutils \
    gawk m4 patch perl python3 texinfo build-essential \
  && apt-get clean \
  && rm -Rf /var/lib/apt/lists/*

ENV WORK_ROOT /work
ENV DIST_DIR /var/tmp
VOLUME ${DIST_DIR}
ENV SCRIPT_DIR /scripts
COPY . ${SCRIPT_DIR}/
RUN ${SCRIPT_DIR}/init.bash
WORKDIR /app

ENTRYPOINT ["./build.bash"]
