#!/usr/bin/python3
from gen_graph import gen
from build_graph_rl import construct_graph
from build_graph_rl import check_and_update_graph
from build_graph_rl import recover
#from dijkstra import dijkstra
from KSP import KSP
from qnet_resource import estimate_resource
import pulp
from read_network_function import read_graph
#from round_and_check import round_and_check
from rounding import rounding
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

K = 3  # the value of K in K shortest paths
l_argv = sys.argv
l_argv.pop(0)
l_demand = list()
for i in l_argv:
    j = i.strip()
    j = j.replace('(','').replace(')','')
    j = j.split(',')
    l_demand.append((int(j[0]),int(j[1]),float(j[2])))
demands = l_demand
#demands = [(1,14,0.8),(2,20,0.85),(3,30,0.85),(6,5,0.8),(15,4,0.85),(11,7,0.85),(29,8,0.8),(25,20,0.85),(11,19,0.8),(12,13,0.85),(30,49,0.8),(29,10,0.8),(31,1,0.8),(5,23,0.5)]
(UG,DG) = gen(100,0.05)
#(DG,UG) = (DG,UG) = read_graph(network)
#(nodes,graph) = construct_graph(UG)
graph = construct_graph(UG) # graph = (node,graph) => node = graph[0], graph => graph[1]
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

    c_kPath = kPath.copy()
    c_l_resource = l_resource.copy()
    for i in range(len(c_kPath)):
        nodes = c_kPath.pop()
        l_node = [n.index for n in nodes]
        #print(f"##### Path: {l_node} #####")
        rs = c_l_resource.pop()   # rs is a dictionary whose keys are edges along the path and value is a list of number of links and fidelity
        for e in rs:
            fidelity = 1
            for ee in e:
                #print(f"The number of required links: {e[ee][0]}")
                fidelity = fidelity*e[ee][1]
            #print(f"The fidelity after scheduling: {fidelity}")

# Describe the required resource for each demand by order
rsc_demand_order = dict()   # key: the order of demand, value: a list of required resource, each element of the list is a dictionary whose keys are edges (address)
                            # and values are the number of required links on these edges
for d in rsc_demand:
    temp_rsc_list = list()
    for rsc in rsc_demand[d]:
        for d_rsc in rsc:
            temp_rsc_list.append(d_rsc)
    rsc_demand_order[d] = temp_rsc_list

# Define the integer linear problem
prob = pulp.LpProblem("Maximize the number of met requests",pulp.LpMaximize)

# Define the variables of the problem
vars = list()   # list of linear program variables
req_rsc_each_d_edge = dict()    # a dictionary whose key is a directed edge (address) and value is a list of tuple whose format is ((demand,path),the number of required links)
num_paths = dict()
for id_d in rsc_demand:
    cnt_path = 0
    for each_list in rsc_demand[id_d]:
        for l_path in each_list:
            vars.append((id_d,cnt_path))
            for edge in l_path:
                if edge not in req_rsc_each_d_edge:
                    req_rsc_each_d_edge[edge] = list()
                req_rsc_each_d_edge[edge].append(((id_d,cnt_path),l_path[edge][0]))
            cnt_path = cnt_path + 1
    num_paths[id_d] = cnt_path

lp_vars = pulp.LpVariable.dicts("Indicator",vars,lowBound=0,upBound=1,cat="Continuous")

temp = list()
for d in range(len(demands)):
    for i in range(num_paths[d]):
        temp.append((lp_vars[d,i],1))

# the objective function
prob += pulp.LpAffineExpression(temp)

for edge in UG.edges:
    temp_1 = list()
    temp_2 = list()
    src = graph[0][edge[0]]
    dst = graph[0][edge[1]]
    for e_temp in graph[1][src]:
        if e_temp.dst == dst:
            e_addr = e_temp
            capacity = e_addr.c
            break
    
    if e_addr in req_rsc_each_d_edge:
        temp_1 = [lp_vars[x[0]]*x[1] for x in req_rsc_each_d_edge[e_addr]]
    
    src = graph[0][edge[1]]
    dst = graph[0][edge[0]]
    for e_temp in graph[1][src]:
        if e_temp.dst == dst:
            e_addr = e_temp
            capacity = e_addr.c
            break

    if e_addr in req_rsc_each_d_edge:
        temp_2 = [lp_vars[x[0]]*x[1] for x in req_rsc_each_d_edge[e_addr]]
        
    if len(temp_1) > 0 and len(temp_2) > 0: # for the cases that the two directions of an edge are both employed
        prob += pulp.lpSum(temp_1) + pulp.lpSum(temp_2) <= capacity
    elif len(temp_1) > 0:   # for the cases that one direction of an edge is employed
        prob += pulp.lpSum(temp_1) <= capacity
    elif len(temp_2) > 0:   # for the cases that one direction, which is opposite to the above, of the edge is employed
        prob += pulp.lpSum(temp_2) <= capacity

for d in range(len(demands)):
    prob += pulp.lpSum([lp_vars[(d,i)] for i in range(num_paths[d])]) <= 1

prob.writeLP("log.txt")
prob.solve()

# print the values of the variables
#for v in prob.variables():
#    print(v.name,"=",v.varValue)

met_demands = list()
for v in vars:
    print(v,"=",lp_vars[v],"=",lp_vars[v].varValue)
    if lp_vars[v].varValue == 1: met_demands.append(v)

print("Met demands:",met_demands)

bk_cap = dict()
# Update the capacity of edges along the entanglement path of the met demands
for d in met_demands:
    c_ok = check_and_update_graph(graph,d,rsc_demand_order,bk_cap)
    if not c_ok: print("Resource problem with demand:",d)

c_vars = vars.copy()
for d in met_demands:
    for v in c_vars:
        if d[0] == v[0]: vars.remove(v)

#for e_addr in req_rsc_each_d_edge:
#    for x in req_rsc_each_d_edge[e_addr]:
#        print(lp_vars[x[0]],"=",lp_vars[x[0]].varValue)

num_met_demands = [x[0] for x in met_demands]
max_addi_met_demands = list()
for cnt in range(20):
    addi_met_demands = list()
    temp_num_met_demands = num_met_demands.copy()
    r_value = rounding(vars,lp_vars)    # perform rounding
#    print(r_value)

    temp_met_demands = [vars[x[0]] for x in list(enumerate(r_value)) if x[1] == 1]

#    print("Temporary met demands:",temp_met_demands)

    bk_cap = dict()
    for d in temp_met_demands:
        if d[0] in temp_num_met_demands: continue
        c_ok = check_and_update_graph(graph,d,rsc_demand_order,bk_cap)
        if c_ok:
            addi_met_demands.append(d)
            temp_num_met_demands.append(d[0])   # update the met demands

    if len(max_addi_met_demands) < len(addi_met_demands): max_addi_met_demands = addi_met_demands
    recover(graph,bk_cap)

for md in max_addi_met_demands:
    met_demands.append(md)

print("Final met demands:",met_demands)

fptr = open("result.txt","a")
fptr.write(f"{len(met_demands)}\n")
fptr.close()

# The status of the solution
print("Status:",pulp.LpStatus[prob.status])

# The value of objective function (optimal value)
print("The value of the objective function:",pulp.value(prob.objective))

finish = 1
print("Finish")
