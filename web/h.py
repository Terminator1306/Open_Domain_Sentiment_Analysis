import random


class Node:
    def __init__(self, weight=0, left=None, right=None):
        self.weight = weight
        self.left = left
        self.right = right


def sort(mlist):
    return sorted(mlist, key=lambda node: node.weight)


def Huffman(mlist):
    while len(mlist) != 1:
        a, b = mlist[0], mlist[1]
        new = Node()
        new.weight = a.weight + b.weight
        new.left, new.right = a, b
        mlist.remove(a)
        mlist.remove(b)
        mlist.append(new)
        mlist = sort(mlist)
    return mlist


def traval(First):
    if First is None:
        return
    traval(First.left)
    print First.weight
    traval(First.right)


def recover(First, max_v):
    if First is None:
        return
    First.weight = max_v - First.weight
    recover(First.right, max_v)
    recover(First.left, max_v)


def compute_weight(First):
    if First.left is None:
        return First.weight
    compute_weight(First.left)
    compute_weight(First.right)
    First.weight = First.left.weight + First.right.weight


mlist = []
max_v = 0
for i in range(6):
    v = random.randint(1, 20)
    if max_v < v:
        max_v = v
    mlist.append(Node(v))
max_v += 1

# mlist = sort(mlist)
# print " ".join([str(node.weight) for node in mlist])
#
# for node in mlist:
#     node.weight = max_v - node.weight
#
# rlist = Huffman(mlist)
#
# recover(rlist[0], max_v)
# compute_weight(rlist[0])
#
# traval(rlist[0])
# print "finish"
