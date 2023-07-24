from gurobipy import *
import logging

def set_problem_size(nodes_list, tasks_list):

    nUsers = 1
    nConstraints = 0
    cpuPercentages = 2

    nTask = len(tasks_list) # Number of tasks
    nNodes = len(nodes_list) # Number of nodes that form the infrastructure

    solver = Model("milp")
    solver.setParam(GRB.Param.NonConvex, 2)

    tasks = [[0 for _ in range(11)] for _ in range(nTask)]
    nodes = [[0 for _ in range(17)] for _ in range(nNodes)]

    return nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes


def set_data_to_transmit(nTask):
    relation = [[0 for _ in range(nTask)] for _ in range(nTask)]
    return relation

# Defining each task that forms the application:
# 0 - CPU cycles, 
# 1 - RAM required (mb), 
# 2 - User (in case of replication for multiple users, 0 by default), 
# 3 - Minimal transmission (in case of requiring a minimal bandwidtk (e.g., for video streaming in a specific quality)), 
# 4 - Sensing requirements (e.g., thermometer), 
# 5 - Peripheral requirements (e.g., camera, GPU), 
# 6 - Transmit
# 7 - Exact location (in case the app is located in a specific place (e.g., dispatch 4.1) 'none' by default), 
# 8 - Type (e.g., sensing mote)
# 9 - Disk required (Mb) 
# 10 - Task name

def set_tasks(nTask, tasks_list):
    tasks = [[0 for _ in range(11)] for _ in range(nTask)]
    
    for x in range(nTask):
        tasks[x][0] = 150000
        tasks[x][1] = 150
        tasks[x][2] = 0
        tasks[x][3] = 0
        tasks[x][4] = {''}
        tasks[x][5] = {''}
        tasks[x][6] = {}
        tasks[x][7] = 'none'
        tasks[x][8] = 'computing'
        tasks[x][9] = 100
        tasks[x][10] = 'name'
    return tasks


def set_rtt(nNodes):
    rtt = [[0.01 for _ in range(nNodes)] for _ in range(nNodes)]
    return rtt

# 0 - CPU (cycles per second)
# 1 - Bandwidth up (bits/s)
# 2 - Power Upload (Ptx), 
# 3 - Maximum energy consumption (Watts) 
# 4 - RAM (Mb)
# 5 - Importance of saving energy in nodes (real number between 0 and 1). In this case, all nodes has been configured with the same node weighting (1) 
# 6 - Power Download (Prx), 
# 7 - Bandwidth Down (bits/s), 
# 8 - Sensing units (e.g., thermomether), '' if any 
# 9 - Peripherals (e.g., GPU), '' if any
# 10 - Type (e.g., sensing mote), 'computing' by default
# 11- Location (e.g., dispatch 2.30),  
# 12 - Owner (e,g., CAOSD group), 'public' by default
# 13 - Communication capacities (e.g., wlan)
# 14 - Number of cores, 
# 15 - Percentage of idle energy consumption, 
# 16 - Percentage of energy consumption in sleeping mode

def set_nodes(nNodes, nodes_list):
    nodes = [[0 for _ in range(17)] for _ in range(nNodes)]
    for x in range(nNodes):
        nodes[x][0] = 10000000
        nodes[x][1] = 150000000
        nodes[x][2] = 0.3
        nodes[x][3] = 75
        nodes[x][4] = 2000
        nodes[x][5] = 1
        nodes[x][6] = 0.7
        nodes[x][7] = 150000000
        nodes[x][8] = {''}
        nodes[x][9] = {''}
        nodes[x][10] = 'computing'
        nodes[x][11] = 'class' + str(x)
        nodes[x][12] = 'public'
        nodes[x][13] = {'wlan'}
        nodes[x][14] = 2
        nodes[x][15] = 30
        nodes[x][16] = 0.01
    return nodes

def setterMain(nodes_list, tasks_list):
    nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes = set_problem_size(nodes_list, tasks_list)
    relation = set_data_to_transmit(nTask)
    nodes = set_nodes(nNodes, nodes_list)
    tasks = set_tasks(nTask, tasks_list)
    rtt = set_rtt(nNodes)
    print (nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt)
    return (nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt)


if __name__ == "__main__":
    setterMain(nodes_list, tasks_list)