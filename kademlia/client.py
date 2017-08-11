#!/usr/bin/env python
# encoding: utf-8

from protocol import KServer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind', help="ipaddr:port this listen to")
parser.add_argument('-p', '--peer', help="ipaddr:port node to connect")
args = parser.parse_args()

ip, port = args.bind.split(":")
if args.peer:
    peerip, peerport = args.peer.split(":")
    node = KServer((ip, int(port)), peer=(peerip, int(peerport)))
else:
    node = KServer((ip, int(port)))
node.serve()
