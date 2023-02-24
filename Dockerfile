FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-dev python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# RUN apt-get update && \
#     apt-get install -y cmake

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:ethereum/ethereum && \
    apt-get update && \
    apt-get install -y solc

WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "src/app.py"]
