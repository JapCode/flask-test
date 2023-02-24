FROM alpine:3.17

RUN apk update && \
    apk add sudo && \
    addgroup -S sudo && \
    adduser -S user && \
    addgroup user sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN apk update && \
    apk add --no-cache python3 python3-dev curl && \
    curl https://bootstrap.pypa.io/get-pip.py | python3 && \
    rm -rf /var/cache/apk/*


RUN apk update && \
    apk add curl tar && \
    curl -LO https://github.com/ethereum/solidity/releases/download/v0.8.18/solidity_0.8.18.tar.gz && \
    tar -xzf solidity_0.8.18.tar.gz && \
    rm solidity_0.8.18.tar.gz && \
    cd solidity_0.8.18 && \
    chmod +x solc && \
    mv solc /usr/local/bin/

RUN chmod +x /usr/local/bin/solc

WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "src/app.py"]