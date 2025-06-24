FROM python:3.13-alpine AS builder

# 安装构建依赖并安装 Python 包
RUN apk add --no-cache --virtual .build-deps \
    gcc g++ make openssl-dev python3-dev libffi-dev autoconf && \
    pip install --no-cache-dir pycryptodome

# 运行阶段使用更小的镜像
FROM python:3.13-alpine

# 从构建阶段复制安装的 Python 包
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

WORKDIR /opt/d3sys

# 复制应用文件
COPY server.py secret.py ./

EXPOSE 10001
CMD ["python", "-u", "server.py"]