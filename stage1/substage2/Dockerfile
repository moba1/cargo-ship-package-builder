FROM scratch

ARG DIST_DIR
ARG ROOT_DIR
COPY ./dist/ /
COPY ./source/ "${DIST_DIR}"
ENV APP_DIR=/app
COPY ./*.bash ./src "${APP_DIR}"/
ENV HOME=/root PATH=/usr/bin:/usr/sbin
ENTRYPOINT [ "/bin/bash", "-l", "+h" ]
