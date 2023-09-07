from gurobipy import *
from gurobipy import Model, GRB
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
    emptySet = createEmpty()

    for x in range(nTask):
        task = tasks_list[x]  # Obtener el diccionario que representa la tarea
        tasks[x][0] = task.get('cpucycles', 150000)
        tasks[x][1] = task.get('ram', 150)
        tasks[x][2] = task.get('user', 0)
        tasks[x][3] = task.get('mintransm', 0)
        tasks[x][4] = set(task.get('sensreq', emptySet))       
        tasks[x][5] = set(task.get('periphreq', emptySet))     
        tasks[x][6] = set(task.get('transmit', emptySet))      
        tasks[x][7] = task.get('exlocation', 'none')
        tasks[x][8] = task.get('tasktype', 'computing')
        tasks[x][9] = task.get('disk', 100)
        tasks[x][10] = task.get('taskname', 'name')
    return tasks

def convertListsToSetsFromMap(myList):
    for i in range(len(myList)):
        if isinstance(myList[i], list):
            myList[i] = set(myList[i])


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
    emptySet = createEmpty()

    for x in range(nNodes):
        node = nodes_list[x]  # Obtener el diccionario que representa el nodo
        nodes[x][0] = node.get('cpu', 10000000)
        nodes[x][1] = node.get('bwup', 150000000)
        nodes[x][2] = node.get('pwup', 0.3)
        nodes[x][3] = node.get('maxenergy', 75)
        nodes[x][4] = node.get('ram', 2000)
        nodes[x][5] = node.get('importance', 1)
        nodes[x][6] = node.get('pwdown', 0.7)
        nodes[x][7] = node.get('bwdown', 150000000)
        nodes[x][8] = set(node.get('sensingunits', emptySet))
        nodes[x][9] = set(node.get('peripherials', emptySet))
        nodes[x][10] = node.get('typecore', 'computing')
        nodes[x][11] = 'class' + str(x) #node.get('class' + str(x))
        nodes[x][12] = node.get('owner', 'public')
        nodes[x][13] = node.get('comcap', {'wlan'})
        nodes[x][14] = node.get('cores', 2)
        nodes[x][15] = node.get('percnormal', 30)
        nodes[x][16] = node.get('percsleeping', 0.01)
    return nodes



def setterMain(nodes_list, tasks_list):
    nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes = set_problem_size(nodes_list, tasks_list)
    relation = set_data_to_transmit(nTask)
    nodes = set_nodes(nNodes, nodes_list)
    tasks = set_tasks(nTask, tasks_list)
    rtt = set_rtt(nNodes)
    #print (nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt)
    return (nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt)


def createEmpty():
        emptySet = set()
        emptySet.add("")
        return emptySet

if __name__ == "__main__":
    from imain import nodes_list, tasks_list
    setterMain(nodes_list, tasks_list)