#!/usr/bin/python3
#from read_network_function import read_graph
#from itertools import permutations
#import networkx as nx
import random
import sys
import numpy as np

#graph = "UsCarrier.graphml"
#mpl = 8
num_demands = 20
num_cases = 100
l_argv = sys.argv
l_argv.pop(0)
num_nodes = int(l_argv.pop())   # normal case: 100 nodes

#(DG,UG) = read_graph(graph)
#nodes = [n for n in range(100)]
#demand_list = list(permutations(nodes,2))
d_fidelity = [0.7,0.75,0.8,0.85,0.9]
for d_f in d_fidelity:
    print(f"Opening file for write, case {d_f}")
    fptr = open(f"Sample_{d_f}.txt",'w')
    
    for k in range(num_cases):
        check_ok = False
        print("Generating fidelity")
        while not check_ok:
            if d_f < 0.9:
                f_temp = np.random.normal(d_f,0.05,num_demands)
            else:
                f_temp = np.random.normal(d_f,0.02,num_demands)
            f_list = list(f_temp)
            #print(f_list)
            if all(i < 1 for i in f_list): check_ok = True
            #print(check_ok)

        temp_list_demand = list()
        print("Generating demands")
        for i in range(num_demands):
            src = random.randint(0,num_nodes-1)
            dst = random.randint(0,num_nodes-1)
            while (src == dst) or (src,dst) in temp_list_demand or (dst,src) in temp_list_demand:
                src = random.randint(0,num_nodes-1)
                dst = random.randint(0,num_nodes-1)
            temp_list_demand.append((src,dst))
        print("Applying fidelity")
        idx = 0
        list_demand = list()
        for d in temp_list_demand:
	    #fidelity = random.uniform(0.75,0.95)
            fidelity = f_list[idx]
            idx = idx + 1
            fptr.write(f"({d[0]},{d[1]},{fidelity}) ")
	        #list_demand.append((d[0],d[1],random.uniform(0.75,0.85)))
	    #fptr.write(str(list_demand))
        if k < num_cases-1: fptr.write("\n")
    print("Closing the file")
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
