import numpy as np
def rounding(vars,lp_vars):
    temp_list = list()
    for x in vars:
        if lp_vars[x].varValue < 0: temp_list.append(0)  # to avoid some situation that negative values are extreme small (nearly equal to zero)
        else: temp_list.append(lp_vars[x].varValue)
    #temp_list = [lp_vars[x].varValue for x in vars]
    #print(temp_list)
    temp_round = np.random.binomial(1,temp_list)
    return list(temp_round)

def half_based_rounding(vars,lp_vars):
    round_value = list()
    temp_list = [lp_vars[x].varValue for x in vars]
    for i in temp_list:
        if i >= 0.5: round_value.append(1)
        else: round_value.append(0)
    return round_value