#!/usr/bin/python3
# Find K shortest paths using Yen algorithm
# Input: a directed graph, source, destination, and K (the undirected graph must be converted to directed graph)
# Output: a set of shortest paths (the number of elements of the set may be less than or equal to K)

from dijkstra import dijkstra
import copy

def build_path(dst):    # dst in object
    path = list()
    if dst.pi == None:
        return None
    else:
        while dst.pi != None:
            path.append(dst)
            dst = dst.pi
        path.append(dst)
        path.reverse()
        return path

def remove_edge(graph,n1,n2):
    temp1 = None
    temp2 = None
    for e in graph[n1]:
        if e.dst == n2:
            temp1 = e
            graph[n1].remove(e)
            break
    for e in graph[n2]:
        if e.dst == n1:
            temp2 = e
            graph[n2].remove(e)
            break
    if temp1 == None and temp2 == None: return None
    temp = (temp1,temp2)
    return temp

def remove_node(graph,node):
    bk_list = list()
    for e in graph[node]:
        for eo in graph[e.dst]:
            if eo.dst == node:
                bk_list.append((e.dst,eo))  # (destination node, edge)
                graph[e.dst].remove(eo)
                break
    bk_list.append(graph[node])
    del graph[node]
    return bk_list

def restore_node(graph,bk_node,bk_node_list):
    while len(bk_node_list) > 0:
        node = bk_node_list.pop()
        temp_list = bk_node[node]
        temp = temp_list.pop()
        graph[node] = temp
        while len(temp_list) > 0:
            temp = temp_list.pop()
            graph[temp[0]].append(temp[1])

def restore_edge(graph,bk_edge):
    for nodes in bk_edge:
        graph[nodes[0]].append(bk_edge[nodes][0])
        graph[nodes[1]].append(bk_edge[nodes][1])

def select_path(graph,B):
    min_w = 1000
    sPath = list()
    for p in B:
        temp = 0
        w = 0
        dst = p[-1]
        while dst.pi != None:
            for e in graph[dst.pi]:
                if e.dst == dst:
                    w = e.w
                    break
            dst = dst.pi
            temp = temp + w
        if min_w > temp:
            min_w = temp
            sPath = p
    return sPath

def KSP(graph, src, dst, K):    # src and dst is the name of the source and the destination (in integer)
                                # graph[0]: list of nodes, graph[1]: graph dictionay (list of edges)
    A = list()  # contains the result
    dijkstra(graph[1],graph[0][src])
    path = build_path(graph[0][dst])    # the first path is the shortest path
    if (path == None): return None      # the case that we cannot find any path from the source to the destination
    A.append(path)
    B = list()
    for k in range(1,K):
        for i in range (len(A[k-1])-1):
            spurNode = A[k-1][i]
            rootPath = A[k-1][:i+1]

            # Remove edge (i,i+1)
            bk_edge = dict()    # backup edges for restoring
            for path_A in A:
                if rootPath == path_A[:i+1]:
                    r_edge = remove_edge(graph[1],path_A[i],path_A[i+1])
                    if r_edge != None:  # if the edge hasn't been removed (the edge may be removed before)
                        bk_edge[(path_A[i],path_A[i+1])] = r_edge # backup edges for restoring
            
            # Remove node along the root path
            bk_node = dict()    # contains the edges that are related to the removed nodes
            bk_node_list = list()   # contains the removed nodes
            for n in rootPath:
                if n != spurNode:
                    bk_node_list.append(n)
                    bk_list = remove_node(graph[1],n)
                    bk_node[n] = bk_list

            dijkstra(graph[1],spurNode)
            spurPath = build_path(graph[0][dst])
            # restore nodes to graph
            restore_node(graph[1],bk_node,bk_node_list)
            # restore edges to graph
            restore_edge(graph[1],bk_edge)
            if spurPath == None: continue
            else:
                del spurPath[0]
                totalPath = rootPath + spurPath
            if totalPath not in B:  B.append(totalPath)
        if len(B) == 0: break
        k_path = select_path(graph[1],B)
        A.append(k_path)
        B.clear()

    return A