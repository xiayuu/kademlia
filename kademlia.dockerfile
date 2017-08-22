FROM python:2.7-slim

WORKDIR /app

add ./build/rpcudp/ /app/rpcudp
add ./build/kademlia/ /app/kademlia

RUN apt update && apt install -y gcc
RUN pip install msgpack-python
RUN cd /app/rpcudp/; python setup.py install




