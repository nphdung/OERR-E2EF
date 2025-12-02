#!/usr/bin/python3
import networkx as nx

def gen(nov,prob):
    check_connected = 0 # use to check if the network is connected. We need to generate a connected network
    s = 0
    while check_connected == 0:
        check_connected = 1
        UG = nx.erdos_renyi_graph(nov,prob,seed=s)
        if not nx.is_connected(UG):
            print("The network is not connected. Generate again")
            check_connected = 0
            s = s+1
        #nodes = list(UG.nodes)
        #edges = list(UG.edges)
        #for n in nodes:
        #    n_connect = 0
        #    for e in edges:
        #        if e[0] == n or e[1] == n:
        #            n_connect = 1
        #            break
        #    if n_connect == 0:
        #        check_connected = 0
        #        print("The network is not connected. Generate again")
        #        break
    temp_edges = list()
    edges = list(UG.edges)
    for e in edges:
        temp_edges.append((e[0],e[1]))
        temp_edges.append((e[1],e[0]))
    DG = nx.DiGraph()
    DG.add_edges_from(temp_edges)
    return (UG,DG)

if __name__ == '__main__':
    (UG,DG) = gen(20,0.2)
    print(DG.nodes)
    print(DG.edges)
    print(UG.nodes)
    print(UG.edges)
