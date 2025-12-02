#!/usr/bin/python3

import sys

num_cases = 100
l_argv = sys.argv
l_argv.pop(0)
test_case = l_argv[1]
num_demands = l_argv[0]
try:
    r_file = open(test_case + num_demands + ".txt","r")
except:
    print(f"Cannot open file: {test_case}{num_demands}.txt")

w_file = open("agg.txt","a")

result = r_file.read()
result = result.split("\n")
result.pop()    # pop the blank

if len(result) != num_cases: print(f"Problem with the result in case: {test_case}, {num_demands}")
else:
    temp_result = [int(x) for x in result]
    ave_result = sum(temp_result)/len(temp_result)
    w_file.write(f"{num_demands}\t{ave_result}\n")

r_file.close()
w_file.close()
