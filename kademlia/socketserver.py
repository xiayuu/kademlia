#!/usr/bin/env python
# encoding: utf-8

from rpcudp.rpcserver import RPCServer, rpccall, rpccall_n
from protocol import KServer
from utils import delay_run
from hashlib import sha1

class SocketServer(KServer):
    def __init__(self, addr, peer=None, port=None):
        super(SocketServer, self).__init__(addr, peer=peer)
        self.port = port
        self.server()

    def getdestnodes(key):
        sha1key = int(sha1(key).hexdigest(), 16)
        nodes = self.rpc_findnode(sha1key, self.dict())
        return self.nodelookup(sha1key, nodes)

    def handle(fd):
        while True:
            x = fd.readline()
            if not x:
                break
            args=x.split(':')
            if args[0] == 'get':
                key = args[1]
                nodes = self.getdestnodes(key)
                values = self.findvalue([n['address'] for n in nodes], key)
                for v,_ in values:
                    if v:
                        fd.write(v)
                        break
                fd.flush()
            elif args[0] == 'set':
                key = args[1]
                value = args[2]
                nodes = self.getdestnodes(key)
                self.store([n['address'] for n in nodes], key, value)
                fd.write('ok')
                fd.flush()

    @delay_run(delay=5)
    def server(self):
        srv = eventlet.listen(('0.0.0.0', self.port))
        pool = eventlet.GreenPool()
        while True:
            try:
                new_sock, address = srv.accept()
                pool.spawn_n(handle, new_sock.makefile('rw'))
            except Exception:
                break




