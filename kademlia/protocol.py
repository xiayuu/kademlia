#!/usr/bin/env python
# encoding: utf-8

from rpcudp.rpcserver import RPCServer, rpccall

KBUCKET_SIZE = 20
TREE_HEIGHT = 159

"""
implement rpc call in  kademlia
"""
class KademliaRpc(RPCServer):

    @rpccall
    def ping(self, dest):
        pass

    @rpccall
    def store(self, dest, keypair):
        pass

    @rpccall
    def findnode(self, dest, key):
        pass

    @rpccall
    def findvalue(self, dest, key):
        pass

class KServer(KademliaRpc):
    def __init__(self):
        self.kbucket = [[]] * TREE_HEIGHT
        self.initserver()

    def initserver(self):
        pass

    def addnode(self, node):
        distance = self.id ^ node['id']

        #find the first big i
        for i in range(TREE_HEIGHT):
            if distance >= pow(2, (TREE_HEIGHT - i )) and \
                    len(self.kbucket[(TREE_HEIGHT - i)]) < KBUCKET_SIZE:
                self.kbucket[(TREE_HEIGHT - i)] = node
                return





