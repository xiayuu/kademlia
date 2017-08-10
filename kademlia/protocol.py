#!/usr/bin/env python
# encoding: utf-8

from rpcudp.rpcserver import RPCServer, rpccall

KBUCKET_SIZE = 20
TREE_HEIGHT = 160
ALPHA = 3

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

    def findclosestk(self, key):
        """return the index of closest kbucket"""
        distance = self.id ^ key

        #find the first big i
        for i in range(0, TREE_HEIGHT):
            if distance < pow(2, i):
                return i

    def addnode(self, node):
        k = self.findclosestk(node['id'])
        if len(self.kbucket[k]) < KBUCKET_SIZE:
            #check if already exist the node
            for n in self.kbucket[k]:
                if n['id'] == node['id']:
                    return
            self.kbucket[k].append(node)

    def rcp_findnode(self, key, node):
        #add node to kbucket
        self.addnode(node)
        res = []
        i, j = self.findclosestk(node['id'])
        res.extend(self.kbucket[i])
        while len(res) < KBUCKET_SIZE:
            i = i - 1
            j = j + 1
            if i >= 0:
                res.extend(self.kbucket[i])
            if j <= TREE_HEIGHT:
                res.extend(self.kbucket[j])
            if i < 0 and j > TREE_HEIGHT:
                break
        return res[:KBUCKET_SIZE]

    def nodelookup(self, key):
        k = self.findclosestk(key)






