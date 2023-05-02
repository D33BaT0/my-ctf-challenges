FROM python:3.10-alpine
LABEL Description="d3sys" VERSION='1.0'

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && apk update && apk add gcc g++ make openssl-dev python3-dev libffi-dev autoconf && mkdir -p /opt/d3sys && pip install pycryptodome -i https://pypi.mirrors.ustc.edu.cn/simple

WORKDIR /opt/d3sys

COPY server.py .
COPY gmssl .
COPY secret.py .

EXPOSE 10001
CMD ["python", "-u", "server.py"]
