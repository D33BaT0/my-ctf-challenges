FROM python:3.13-alpine

WORKDIR /home/ctf

RUN apk add --no-cache socat && \
    addgroup -S ctf && adduser -S -G ctf ctf && \
    chmod 1733 /tmp /var/tmp /dev/shm && \
    pip install --no-cache-dir pycryptodome sympy numpy

COPY --chown=ctf:root file/ .
RUN chmod 500 ./server.py

USER ctf

EXPOSE 11420
CMD socat TCP-L:11420,fork,reuseaddr EXEC:"python3 ./server.py",pty,stderr,setsid,sane,raw,echo=0

 