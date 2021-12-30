FROM scratch

ARG DIST_DIR
COPY ./dist/ /
COPY ./source/ "${DIST_DIR}"
ENV APP_DIR=/app
COPY ./*.bash "${APP_DIR}"/
COPY ./src "${APP_DIR}"/src
ENV HOME=/root PATH=/usr/bin:/usr/sbin
ENTRYPOINT [ "/bin/bash", "-l", "+h" ]
