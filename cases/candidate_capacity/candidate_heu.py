#!/usr/bin/python3
from gen_graph import gen
from build_graph_capacity import construct_graph
from build_graph_capacity import check_and_update_graph
#from dijkstra import dijkstra
from KSP import KSP
from qnet_resource import estimate_resource
import pulp
from read_network_function import read_graph
#from round_and_check import round_and_check
from rounding import rounding
from rounding import half_based_rounding
import sys

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

def print_path(dst):
    if dst.pi != None: print_path(dst.pi)
    print(f"{dst.index} ",end="")

network = "Surfnet.graphml.xml"

l_argv = sys.argv
l_argv.pop(0)
K_temp = l_argv.pop()
K = int(K_temp)
cap = l_argv.pop()
capacity = int(cap)
#K = 3  # the value of K in K shortest paths
num_nodes = 60
l_demand = list()
for i in l_argv:
    j = i.strip()
    j = j.replace('(','').replace(')','')
    j = j.split(',')
    l_demand.append((int(j[0]),int(j[1]),float(j[2])))
demands = l_demand
#demands = [(1,14,0.8),(2,20,0.85),(3,30,0.85),(6,5,0.8),(15,4,0.85),(11,7,0.85),(29,8,0.8),(25,20,0.85),(11,19,0.8),(12,13,0.85),(30,49,0.8),(29,10,0.8),(31,1,0.8),(5,23,0.5)]
(UG,DG) = gen(num_nodes,0.05)
#(DG,UG) = (DG,UG) = read_graph(network)
#(nodes,graph) = construct_graph(UG)
graph = construct_graph(UG,capacity) # graph = (node,graph) => node = graph[0], graph => graph[1]
#for n in graph[1]:
#    print(f"Node: {n.index}")
#    for e in graph[1][n]:
#        print(f"Edge: {n.index,e.dst.index}, fidelity: {e.f}, weight: {e.w}, capacity: {e.c}")

rsc_demand = dict()
idx = 0
for d in demands:
    src = d[0]
    dst = d[1]
    F_th = d[2]

#    print(f"Demand: ({src},{dst}), Threshold: {F_th}")

    kPath = KSP(graph,src,dst,K)   # KSP returns a list of paths, each path include a list of nodes along the path
    if kPath == None: print(f"Cannot find any path from {src} to {dst}")
    else:

    # Next step: estimate the requirement of resource (the number of links) for each demand
        l_resource = estimate_resource(graph[1],kPath,F_th)     # Input: graph, K shortest paths, and the threhold of fidelity
                                                                # Return: a list of list of path , the format of each element of the innermost list: [number of required links, the corresponding fidelity to the schedule]                                                    

    rsc_demand[idx] = l_resource
    idx = idx+1

# Describe the required resource for each demand by order
rsc_demand_order = dict()   # key: the order of demand, value: a list of required resource, each element of the list is a dictionary whose keys are edges (address)
                            # and values are the number of required links on these edges
for d in rsc_demand:
    temp_rsc_list = list()
    for rsc in rsc_demand[d]:
        for d_rsc in rsc:
            temp_rsc_list.append(d_rsc)
    rsc_demand_order[d] = temp_rsc_list

c_demands = demands.copy()
c_rsc_demand_order = rsc_demand_order.copy()
m_demand = list()
while len(c_demands) > 0:
    sort_list = list()
    for d in c_rsc_demand_order:
        if d in m_demand: continue
        if len(c_rsc_demand_order[d]) == 0:
            if demands[d] in c_demands: c_demands.remove(demands[d])    # if there is not any candidate paths for demand d, it cannot be satisfied, just remove it from the list
            continue
        rsc_temp = c_rsc_demand_order[d]
        temp = 0
        for e,rsc in rsc_temp[0].items():
            temp = temp + rsc[0]
        sort_list.append((temp,d))
    if len(sort_list) > 0:
        sort_list.sort()
        select_demand = sort_list[0][1]
        met_demand = (select_demand,0)
        c_ok = check_and_update_graph(graph,met_demand,rsc_demand_order)
        if c_ok:    # if there is enough resource, remove the selected demand from the set of demands
            m_demand.append(select_demand)  # add selected demand to the met demands list
            c_demands.remove(demands[select_demand])    # remove the selected demand from the original demand list
        c_rsc_demand_order[select_demand].pop(0)  # remove the examined candidate path

print("Met demands:",m_demand)

fptr = open("result.txt","a")
fptr.write(f"{len(m_demand)}\n")
fptr.close()

finish = 1
print("Finish")
