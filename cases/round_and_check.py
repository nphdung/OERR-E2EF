# This approach takes a long time to completes, hence not be appropriate to quantum networks
import numpy as np
def round_and_check(UG,graph,req_rsc_each_d_edge,vars,lp_vars,demands):
    check = False
    temp_list = [lp_vars[x].varValue for x in vars]
    while not check:
        # rounding
        temp_round = np.random.binomial(1,temp_list)
        # checking
        # check the first constraint
        check_c1 = True
        e2 = 0
        for e in list(UG.edges):
            src = graph[0][e[0]]
            dst = graph[0][e[1]]
            for e_temp in graph[1][src]:
                if e_temp.dst == dst:
                    e1 = e_temp
                    break

            for e_temp in graph[1][dst]:
                if e_temp.dst == src:
                    e2 = e_temp
                    break

            capacity = e2.c
            temp_1 = 0
            if e1 in req_rsc_each_d_edge:
                for temp in req_rsc_each_d_edge[e1]:
                    id = vars.index(temp[0])
                    temp_1 = temp_1 + temp_round[id]*temp[1]
            if e2 in req_rsc_each_d_edge:
                for temp in req_rsc_each_d_edge[e2]:
                    id = vars.index(temp[0])
                    temp_1 = temp_1 + temp_round[id]*temp[1]
            if temp_1 > capacity:
                check_c1 = False
                break
        if not check_c1: continue

        # check the second constraint
        check_c2 = True
        for d in range(len(demands)):
            p = 0
            temp = 0
            while (d,p) in vars:
                id = vars.index((d,p))
                temp = temp + temp_round[id]
                p = p+1
            
            if temp > 1:
                check_c2 = False
                break
        
        if not check_c2: continue
        
        check = True

    return temp_round