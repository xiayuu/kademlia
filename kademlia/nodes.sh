#!/bin/bash

python client.py -b `ip -4 addr show eth0 | grep /24 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'`:8090 -p bootnode:8090
