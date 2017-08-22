#!/bin/bash
rm -fr build
mkdir build
git clone https://github.com/xiayuu/rpcudp.git build/rpcudp
git clone https://github.com/xiayuu/kademlia.git build/kademlia
docker build -t kademlia -f kademlia.dockerfile .
