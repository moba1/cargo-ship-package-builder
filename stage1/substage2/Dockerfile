FROM scratch

COPY ./dist/ /
ENV HOME=/root PATH=/usr/bin:/usr/sbin
ENTRYPOINT [ "/bin/bash", "-l", "+h" ]
