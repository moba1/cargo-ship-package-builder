FROM scratch

ARG DIST_DIR
COPY ./dist/ /
COPY ./source/ "${DIST_DIR}"
ENV APP_DIR=/app
COPY ./src "${APP_DIR}"/
ENV HOME=/root PATH=/usr/bin:/usr/sbin
ARG TARGET
ARG PROCESS_NUMBER
RUN bash -l +h /app/main.bash \
  && rm -Rf "${DIST_DIR}" "${APP_DIR}" \
  && bash -c "rm -Rf /usr/share/{info,man,doc}/*; find /usr/{lib,libexec} -name \\*.la -delete" \
  && rm -Rf /tools
CMD [ "/bin/bash" ]
