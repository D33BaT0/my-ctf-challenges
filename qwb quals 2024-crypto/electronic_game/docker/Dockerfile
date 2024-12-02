FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y socat python3 python3-pip sagemath
RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN sage -pip install pycryptodome

WORKDIR /home/ctf

ADD file/ .
RUN chmod 500 ./server.py
RUN chown ctf:root . -R

USER ctf
CMD socat TCP-L:11420,fork,reuseaddr EXEC:"sage -python ./server.py",pty,stderr,setsid,sane,raw,echo=0
EXPOSE 11420
