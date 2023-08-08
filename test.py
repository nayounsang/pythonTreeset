from redblacktree import treeset
import random as rd
import networkx as nx
import matplotlib.pyplot as plt

t = rbtree()

'''
def make_tree(t):
    result = {}
    stack = [t.root]
    while stack:
        idx = stack.pop()
        if t.mem[idx].left is not None:
            stack.append(t.mem[idx].left)
            if idx in result:
                result[idx].append(t.mem[idx].left)
            else:
                result[idx] = [t.mem[idx].left]
        if t.mem[idx].right is not None:
            stack.append(t.mem[idx].right)
            if idx in result:
                result[idx].append(t.mem[idx].right)
            else:
                result[idx] = [t.mem[idx].right]
    return result


def vistree(dic,num):
    print('-----------add',num)
    for node in dic:
        for n in dic[node]:
            print(node, n)
    c = {}
    for node in range(len(t)):
        c[node] = 'red' if t.mem[node].color else 'black'
    print(c)
'''


