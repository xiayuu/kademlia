#!/usr/bin/env python
# encoding: utf-8

from rpcudp.rpcserver import RPCServer, rpccall, rpccall_n
from utils import period_task
from hashlib import sha1

KBUCKET_SIZE = 20
TREE_HEIGHT = 160
ALPHA = 3

"""
implement rpc call in  kademlia
"""
class KademliaRpc(RPCServer):

    @rpccall_n(timeout=1)
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
        super(KademliaRpc, self).__init__(DEBUG=True)
        self.addr = addr[1]
        self.id = int(addr[0], 16)
        self.kbucket = [[]] * (TREE_HEIGHT + 1)
        self.stores = {}
        self.initserver(peer)
        self.report_kbucket()
        self.check_tree()

    def dict(self):
        return {"id": str(self.id), "address": self.addr}

    @period_task(period=10)
    def report_kbucket(self):
        i = 0
        for k in self.kbucket:
            for n in k:
                print("%d--%d--%s--%s" % (self.id, i, n['id'], n['address'][0]))
            i = i + 1
        print(self.stores)

    @period_task(period=100)
    def check_tree(self):
        res = self.ping([n['address'] for b in self.kbucket for n in b])
        for r,d in res:
            if not r:
                self.delnode(d)

    @period_task(period=150)
    def republish(self):
        for key in self.stores():
            nodes = self.getdestnodes(key)
            self.store([n['address'] for n in nodes], key, self.stores[key])

    def serve(self):
        self.run(self.addr)

    def initserver(self, peer):
        self.addnode(self.dict())
        if peer:
            nodes = self.rpc_findnode(self.id,
                                      {"id": str(int(peer[0],16)), "address": peer[1]})
            self.nodelookup(self.id, nodes, [])

    def getdestnodes(self, key):
        sha1key = int(sha1(key).hexdigest(), 16)
        nodes = self.rpc_findnode(sha1key, self.dict())
        return self.nodelookup(sha1key, nodes, [])

    def findclosestk(self, key):
        """return the index of closest kbucket"""
        distance = self.id ^ key
        #find the first big i
        for i in range(0, TREE_HEIGHT+1):
            if distance < pow(2, i):
                return i

    def addnode(self, node):
        k = self.findclosestk(int(node['id']))
        if len(self.kbucket[k]) < KBUCKET_SIZE:
            #check if already exist the node
            for n in self.kbucket[k]:
                if n['id'] == node['id']:
                    return
            if self.kbucket[k] == []:
                self.kbucket[k] = [node]
            else:
                self.kbucket[k].append(node)

    def delnode(self, addr):
        for b in self.kbucket:
            for n in b:
                if n['address'] == addr:
                    b.remove(n)
                    return

    def rpc_ping(self):
        return "PONG"

    def rpc_findnode(self, key, node):
        #add node to kbucket
        self.addnode(node)
        res = []
        i = j = self.findclosestk(int(key))
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
        if key in self.stores:
            return self.stores[key]

    def rpc_store(self, key, value):
        self.stores[key] = value

    def nodelookup(self, key, nodes, checkednodes):
        newnode = []
        checkednodes.extend(nodes)
        res = self.findnode([x['address'] for x in nodes], str(key), self.dict())
        for n in [ n for r,d in res if r for n in r if n not in checkednodes]:
            if n not in newnode:
                newnode.append(n)

        newnode.sort(key=lambda node : int(node['id']) ^ key)
        for node in newnode:
            self.addnode(node)

        if len(newnode) == 0:
            checkednodes.sort(key=lambda node : int(node['id']) ^ key)
            return checkednodes[:ALPHA]
        else:
            return self.nodelookup(key, newnode[:ALPHA], checkednodes)







