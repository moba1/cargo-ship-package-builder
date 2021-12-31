ARG STAGE1_IMAGE
FROM "${STAGE1_IMAGE}"

ARG PROCESS_NUMBER
ARG DIST_DIR
ARG ARCH
COPY ./source "${DIST_DIR}"
ENV APP_DIR=/app
COPY ./*.bash "${APP_DIR}"/
COPY ./builder "${APP_DIR}/builder"
RUN bash /app/main.bash \
  && bash -c "rm -Rf /app /var/tmp*"
CMD ["/bin/bash"]
