#!/usr/bin/env python
# encoding: utf-8

from socketserver import SocketServer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind', help="id:ipaddr:port this listen to")
parser.add_argument('-p', '--peer', help="id:ipaddr:port node to connect")
parser.add_argument('-s', '--socketserver', help="port, get:key, set:key:value")
args = parser.parse_args()

id, ip, port = args.bind.split(":")
if args.peer:
    peerid, peerip, peerport = args.peer.split(":")
    node = SocketServer((id, (ip, int(port))), peer=(peerid, (peerip, int(peerport))), port=int(args.socketserver))
else:
    node = SocketServer((id, (ip, int(port))), port=int(args.socketserver))

node.serve()
