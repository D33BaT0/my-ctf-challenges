FROM alpine:3.18 AS builder

RUN apk add --no-cache \
    build-base \
    clang \
    make

COPY src/ /opt/challenge/src/
COPY Makefile /opt/challenge/

WORKDIR /opt/challenge
RUN make

FROM alpine:3.18

RUN apk add --no-cache \
    socat \
    libstdc++ \
    libgcc

RUN adduser -D -s /bin/sh user

COPY --from=builder /opt/challenge/build/Spad3kapig /usr/local/bin/spadesace

RUN chmod +x /usr/local/bin/spadesace

USER user
WORKDIR /home/user

EXPOSE 12312

CMD ["socat", "TCP-LISTEN:12312,fork,reuseaddr", "EXEC:/usr/local/bin/spadesace"]