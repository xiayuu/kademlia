#!/usr/bin/env python
# encoding: utf-8

from protocol import KServer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind', help="id:ipaddr:port this listen to")
parser.add_argument('-p', '--peer', help="id:ipaddr:port node to connect")
args = parser.parse_args()

id, ip, port = args.bind.split(":")
if args.peer:
    peerid, peerip, peerport = args.peer.split(":")
    node = KServer((id, (ip, int(port))), peer=(peerid, (peerip, int(peerport))))
else:
    node = KServer((id, (ip, int(port))))
node.serve()
