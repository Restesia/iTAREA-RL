from gurobipy import *

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


def set_tasks(nTask):
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


def set_nodes(nNodes):
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
    nodes = set_nodes(nNodes)
    tasks = set_tasks(nTask)
    rtt = set_rtt(nNodes)
    print (nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt)
    return (nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt)


if __name__ == "__main__":
    setterMain(nodes_list, tasks_list)