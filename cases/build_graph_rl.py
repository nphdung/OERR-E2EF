#!/usr/bin/python3
# Construct the graph towards object
# Input: an undirected graph, which includes the lists of vertices and edges
# Note: The vertices are arranged in order. Namely, vertex 0 in position 0, vertex 1 in position 1, ...
# Output: the lists of objects of vertices and edges

import random
import math
if __name__ == '__main__':
    from gen_graph import gen
    import networkx as nx

class node:
    def __init__(self,index=None,pi=None,d=None):
        self.index = index
        self.pi = pi
        self.d = d

class edge: # three properties of edge is: edge.dst (a node in object of graph), w (real), and f (real)
    def __init__(self,src=None,dst=None,w=None,f=None,c=None):
        self.dst = dst
        self.src = src
        self.w = w
        self.f = f
        self.c = c

def construct_graph(G):
    nodes = list()
    graph = dict()
    temp_n = list(G.nodes)
    temp_n.sort()
    for n in temp_n:
        #print(n)
        temp_node = node(index=n)
        nodes.append(temp_node)
    s = 0
    for e in G.edges:
        random.seed(s)
        s = s + 1
        f = random.uniform(0.7,0.95)
        w = -math.log(f)
        c = random.randint(1,5)
        if nodes[e[0]] not in graph:
            graph[nodes[e[0]]] = list()
        temp_edge = edge(src=nodes[e[0]],dst=nodes[e[1]],w=w,f=f,c=c)
        graph[nodes[e[0]]].append(temp_edge)
        if nodes[e[1]] not in graph:
            graph[nodes[e[1]]] = list()
        temp_edge = edge(src=nodes[e[1]],dst=nodes[e[0]],w=w,f=f,c=c)
        graph[nodes[e[1]]].append(temp_edge)

    return(nodes,graph) # return the list of nodes and the directed graph expressed by a dictionary
# List of nodes: nodes = |node 0 (object)|node 1 (object)|node 2 (object)| ...... (in order)
# Directed graph: graph = { node 0 (object): (edge 0, edge 1, ...),
#                           ......................................
#                           node n (object): (edge k, edge (k+1), ...) }
# the list of key (node) of the graph dictionary may be not in order

def check(met_demand,rsc_demand_order):
    d = met_demand[0]
    p = met_demand[1]
    rsc = rsc_demand_order[d][p]
    for e in rsc:
        if e.c < rsc[e][0]: return False
    return True 

def check_and_update_graph(graph,met_demand,rsc_demand_order,bk_cap):
    c_ok = check(met_demand,rsc_demand_order)
    if c_ok:    # if the resource is enough, update the graph
        d = met_demand[0]
        p = met_demand[1]
        rsc = rsc_demand_order[d][p]    # dictionary of resource (edge: [links,fidelity])
        for e in rsc:
            if e not in bk_cap:
                bk_cap[e] = e.c
            src = e.src
            dst = e.dst
            e.c = e.c - rsc[e][0]   # update forward edge
            for e_temp in graph[1][dst]:
                if e_temp.dst == src:
                    e_temp.c = e_temp.c - rsc[e][0] # update backward edge
                    break
        return True
    else: return False  # if the resource is not enough, return False

def recover(graph,bk_cap):
    for e in bk_cap:
        src = e.src
        dst = e.dst
        for e_temp in graph[1][src]:
            if e_temp.dst == dst:
                e_temp.c = bk_cap[e]
                break
        for e_temp in graph[1][dst]:
            if e_temp.dst == src:
                e_temp.c = bk_cap[e]
                break

if __name__ == '__main__':
    (UG,DG) = gen(20,0.6)
    (nodes,graph) = construct_graph(UG)
    for n in graph:
        print(f"Node: {n.index}")
        for e in graph[n]:
            print(f"Edge: {n.index,e.dst.index}, fidelity: {e.f}, weight: {e.w}")