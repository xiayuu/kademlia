#!/usr/bin/env python
# encoding: utf-8

from rpcudp.rpcserver import RPCServer, rpccall

KBUCKET_SIZE = 20
TREE_HEIGHT = 160

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
    def findnode(self, dest, key, node):
        pass

    @rpccall
    def findvalue(self, dest, key):
        pass

class KServer(KademliaRpc):
    def __init__(self):
        self.kbucket = [[]] * (TREE_HEIGHT + 1)
        self.initserver()

    def initserver(self):
        self.addnode(self.dict())

    def findclosestk(self, node):
        """return the index of closest kbucket"""
        distance = self.id ^ node['id']

        #find the first big i
        for i in range(0, TREE_HEIGHT):
            if distance < pow(2, i):
                return i

    def addnode(self, node):
        k = self.findclosestk(node)
        if len(self.kbucket[k]) < KBUCKET_SIZE:
            #check if already exist the node
            for n in self.kbucket[k]:
                if n['id'] == node['ide']:
                    return
            self.kbucket[k].append(node)

    def rcp_findnode(self, key, node):
        #add node to kbucket
        self.addnode(node)

        k = self.findclosestk(node)
        if len(self.kbucket[k])




