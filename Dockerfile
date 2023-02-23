FROM alpine:3.17

RUN apk update && \
    apk add --no-cache python3 python3-dev curl && \
    curl https://bootstrap.pypa.io/get-pip.py | python3 && \
    rm -rf /var/cache/apk/*

WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "src/app.py"]