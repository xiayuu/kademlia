#!/bin/bash
GKEY=f442001b2a9837f4a03db456ef5623476df141a7
NODEKEY=$(hostname | sha1sum | awk '{print $1}')
python client.py -b ${NODEKEY}:127.0.0.1:8090 -p ${GKEY}:127.0.0.1:8091
