#!/usr/bin/env python
# encoding: utf-8

from rpcudp.rpcserver import RPCServer, rpccall, rpccall_n
import hashlib

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

    @rpccall_n(timeout=1)
    def store(self, dest, keypair):
        pass

    @rpccall_n(timeout=1)
    def findnode(self, dest, key, node):
        pass

    @rpccall_n(timeout=1)
    def findvalue(self, dest, key):
        pass

class KServer(KademliaRpc):
    def __init__(self, addr, peer=None):
        super(KademliaRpc, self).__init__(DEBUG=False)
        self.addr = addr
        self.id = int(hashlib.sha1(addr[0]).hexdigest(), 16)
        self.kbucket = [[]] * (TREE_HEIGHT + 1)
        self.initserver(peer)

    def dict(self):
        return {"id": str(self.id), "address": self.addr}

    def serve(self):
        self.run(self.addr)

    def initserver(self, peer):
        self.addnode(self.dict())
        if peer:
            self.nodelookup(self.id, [{"address": peer}])

    def findclosestk(self, key):
        """return the index of closest kbucket"""
        distance = self.id ^ key

        #find the first big i
        for i in range(0, TREE_HEIGHT):
            if distance < pow(2, i):
                return i

    def addnode(self, node):
        k = self.findclosestk(int(node['id']))
        if len(self.kbucket[k]) < KBUCKET_SIZE:
            #check if already exist the node
            for n in self.kbucket[k]:
                if n['id'] == node['id']:
                    return
            self.kbucket[k].append(node)

    def rpc_findnode(self, key, node):
        #add node to kbucket
        self.addnode(node)
        res = []
        i, j = self.findclosestk(int(key))
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

    def rpc_findvalue(self, key):
        pass

    def rpc_store(self, key, value):
        pass

    def nodelookup(self, key, nodes, checkednodes=[]):
        newnode = []
        checkednodes.extend(nodes)
        res = self.findnode([x['address'] for x in nodes], str(key), self.dict())

        newnode.extend([n for n in [r[0] for r in res if r[0]] if n not in checkednodes])
        newnode.sort(key=lambda node : int(node['id']) ^ key)
        for node in newnode:
            self.addnode(node)

        if len(newnode) == 0:
            return nodes
        else:
            self.nodelookup(key, newnode[:KBUCKET_SIZE], checkednodes)







