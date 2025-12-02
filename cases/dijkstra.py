#!/usr/bin/python3
INF = 1000
def init_single_src(G,s):
    for v in G:
        v.d = INF
        v.pi = None
    s.d = 0

def extract_min(Q):
    index = 0
    min = Q[index].d
    for element in Q:
        if element.d < min:
            index = Q.index(element)
            min = Q[index].d
    return index

def relax(u,v,w):
    if v.d > u.d + w:
        v.d = u.d + w
        v.pi = u

def dijkstra(G,s):
    # Initialize Single Source
    init_single_src(G,s)
    Q = list()
    for v in G:
        Q.append(v)
    while len(Q) > 0:
        min_index = extract_min(Q)
        u = Q.pop(min_index)
        for edge in G[u]:
            relax(u,edge.dst,edge.w)