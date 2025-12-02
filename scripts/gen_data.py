#!/usr/bin/python3
#from read_network_function import read_graph
#from itertools import permutations
#import networkx as nx
import random
import sys

#graph = "UsCarrier.graphml"
#mpl = 8
num_demands = 70
num_cases = 100
l_argv = sys.argv
l_argv.pop(0)
num_nodes = int(l_argv.pop())

#(DG,UG) = read_graph(graph)
#nodes = [n for n in range(100)]
#demand_list = list(permutations(nodes,2))
fptr = open(f"Sample_{num_nodes}.txt",'w')

for k in range(num_cases):
    temp_list_demand = list()
    for i in range(num_demands):
        src = random.randint(0,num_nodes-1)
        dst = random.randint(0,num_nodes-1)
        while (src == dst) or (src,dst) in temp_list_demand or (dst,src) in temp_list_demand:
            src = random.randint(0,num_nodes-1)
            dst = random.randint(0,num_nodes-1)
        temp_list_demand.append((src,dst))
    list_demand = list()
    for d in temp_list_demand:
        fidelity = random.uniform(0.75,0.95)
        fptr.write(f"({d[0]},{d[1]},{fidelity}) ")
        #list_demand.append((d[0],d[1],random.uniform(0.75,0.85)))
    #fptr.write(str(list_demand))
    if k < num_cases-1: fptr.write("\n")
fptr.close()
#
#
#for num_demands in range(2,21):
#    for num in range(num_per_case):
#        d_list = list()
#        i = 0
#        while (i < num_demands):
#            (s,t) = demand_list[random.randrange(len(demand_list))]
#            if (s,t) not in d_list and (t,s) not in d_list and len(nx.dijkstra_path(DG,s,t)) <= mpl:
#                d_list.append((s,t))
#                fptr.write("({},{})".format(s,t))
#                i = i + 1
#                if i < num_demands: fptr.write(" ")
#            else: continue
#        fptr.write("\n")
#fptr.close()
