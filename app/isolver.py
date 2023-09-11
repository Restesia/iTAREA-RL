from gurobipy import *
from gurobipy import quicksum
from gurobipy import GRB

def solverMain(tasks, nodes, relation, rtt, nConstraints, nTask, nNodes, cpuPercentages, solver, communicationCost, communicationCostDown, computationCost, communicationTime, computationTime, cores, assignment, percentageCPU, percentageCPUaux, constraints):
    for t in range(nTask):
        solver.addConstr(quicksum(assignment[t][n] for n in range(nNodes)) == 1)

        for n in range(nNodes):
            solver.addConstr(((assignment[t][n]) * (tasks[t][4] <= nodes[n][8]) *
                              (tasks[t][5] <= nodes[n][9]) * (tasks[t][3] <= nodes[n][1]) *
                              (tasks[t][8] == nodes[n][10]) *
                              ((tasks[t][7] == 'none') + (tasks[t][7] == nodes[n][11])) ==
                              assignment[t][n]))
            solver.addConstr(percentageCPU[n][t] == percentageCPU[n][t] * assignment[t][n])

    for n in range(nNodes):
        for t in range(nTask):
            solver.addConstr((percentageCPU[n][t] * percentageCPUaux[n][t]) == assignment[t][n])

    for m in range(nNodes):
        solver.addConstr(quicksum(percentageCPU[m]) <= cpuPercentages * nodes[m][14])
        solver.addConstr(quicksum(assignment[t][m] * tasks[t][1] for t in range(nTask)) <= nodes[m][4])

    for c in range(nConstraints):
        solver.addConstr(communicationTime ==
                         quicksum(
                             quicksum(
                                 quicksum(
                                     assignment[constraints[c][i]][m] * (1 - assignment[constraints[c][j]][m]) *
                                     (((relation[constraints[c][i]][constraints[c][j]] * 1000000) /
                                       nodes[m][1]) + (rtt[0][0] * 1000000))
                                     for j in range(2, 2 + constraints[c][1]))
                                 for i in range(2, 2 + constraints[c][1]))
                             for m in range(nNodes)))
        solver.addConstr(computationTime ==
                         quicksum(
                             quicksum(
                                 (assignment[constraints[c][i]][m] * (
                                             (tasks[constraints[c][i]][0] * 1000000) *
                                             percentageCPUaux[m][constraints[c][i]] * nodes[m][14] *
                                             cpuPercentages)) / nodes[m][0]
                                 for i in range(2, 2 + constraints[c][1]))
                             for m in range(nNodes)))
        solver.addConstr((computationTime + communicationTime) <= (constraints[c][0] * 1000000))

    solver.addConstr(communicationCost ==
                     quicksum(
                         quicksum(
                             quicksum(
                                 assignment[i][m] * (1 - assignment[j][m]) * (
                                             nodes[m][2] * (relation[i][j] / nodes[m][1]) *
                                             nodes[m][5])
                                 for j in range(nTask))
                             for i in range(nTask))
                         for m in range(nNodes)))
    solver.addConstr(computationCost ==
                     quicksum(
                         quicksum(
                             assignment[i][m] * ((100 - nodes[m][15]) / 100) * nodes[m][3] * (
                                         (tasks[i][0] * 10000) / nodes[m][0])
                             for i in range(nTask))
                         for m in range(nNodes)))
    solver.addConstr(communicationCostDown ==
                     quicksum(
                         quicksum(
                             quicksum(
                                 assignment[i][m] * (1 - assignment[j][m]) * (
                                             nodes[m][6] * (relation[j][i] / nodes[m][7]) *
                                             nodes[m][5])
                                 for j in range(nTask))
                             for i in range(nTask))
                         for m in range(nNodes)))

    solver.addConstr(cores ==
                     quicksum(
                         quicksum(
                             percentageCPU[m][t]
                             for t in range(nTask))
                         for m in range(nNodes)))

    solver.setObjectiveN(communicationCost + communicationCostDown + computationCost, 0, GRB.MINIMIZE)
    solver.setObjectiveN(cores, 1, GRB.MINIMIZE)

    solver.optimize()
    return solver

if __name__ == "__main__":
    from imain import tasks, nodes, relation, rtt, nConstraints, nTask, nNodes, cpuPercentages, solver
    solverMain(tasks, nodes, relation, rtt, nConstraints, nTask, nNodes, cpuPercentages, solver)