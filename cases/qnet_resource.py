#!/usr/bin/python3
# input: directed graph, a list of K shortest got from Yen algorithm

def estimate_resource(graph,kPath,F_th):
    list_resource = list()
    #list_path = list()
    for path in kPath:
        # determine edges along the path
        edge_list = list()  # list of edges along the path
        for i in range(len(path)-1):
            for edge in graph[path[i]]:
                if edge.dst == path[i+1]:
                    edge_list.append(edge)
                    break
        path_fidelity = compute_fidelity(edge_list)
        path_nodes = [n.index for n in path]
        if path_fidelity >= F_th:
            dict_path = dict()
            #print(f"Path {path_nodes}, fidelity: {path_fidelity}, satisfied")
            for e in edge_list:
                dict_path[e] = [1,e.f]
            list_resource.append([dict_path])
            #list_path.append(path)
        else:
            #print(f"Path {path_nodes}, fidelity: {path_fidelity}, not satisfied")
            #for e in edge_list:
            #    dict_path[e] = 0
            # estimate the requirement of resource need to satisfy the constraint of fidelity
            sc = pur_sc(edge_list,F_th)
            list_resource.append(sc)
            #list_path.append(path)
    return list_resource

def compute_fidelity(edge_list):
    fidelity = 1
    for edge in edge_list:
        fidelity = fidelity*edge.f
    return fidelity

def pur_sc(edge_list,F_th):
    meet_schedule = list()  # a list of dictionary that contains the list of the met schedules
                            # each element is a dictionary with the keys are edges and the value is a list
                            # that contains the requirement resource (the number of necessary links) and the corresponding fidelity
    max_f = 0
    meet = False
    temp_dict = dict()
    for e in edge_list:
        temp_dict[e] = [1,e.f]  # initial value of schedule (the number of necessary links = 1, fidelity = e.f)
    
    while not meet:
        for e in edge_list:
            pur_e = purify(temp_dict[e][1],e.f) # conduct the purification on edge e
            temp_fidelity = pur_e
            # compute the end to end fidelity
            for temp_e in edge_list:
                if temp_e != e:
                    temp_fidelity = temp_fidelity*temp_dict[temp_e][1]

            # if the e2e fidelity is still less than the threshold and the fidelity constraint is not met
            if (temp_fidelity < F_th):
                if not meet and (temp_fidelity > max_f):
                    max_f = temp_fidelity
                    bk_schedule = [e,temp_dict[e][0]+1,pur_e]    # add the new schedule
            else:   # if the e2e fidelity is greater than or equal to the threshold
                if not meet: meet = True # met the constraint
                bk_e = temp_dict[e]
                #temp_dict[e] = [temp_dict[e][0]+1,pur_e]
                copy_dict = temp_dict.copy()
                copy_dict[e] = [copy_dict[e][0]+1,pur_e]
                #meet_schedule.append(temp_dict)
                meet_schedule.append(copy_dict)
                #temp_dict[e] = bk_e
        
        if not meet:
            temp_dict[bk_schedule[0]] = bk_schedule[1:3]
    
    return meet_schedule

def purify(fidelity,org_fidelity):
    temp1 = fidelity*org_fidelity
    temp2 = (1-fidelity)*(1-org_fidelity)
    pur_fidelity = temp1/(temp1+temp2)
    return pur_fidelity