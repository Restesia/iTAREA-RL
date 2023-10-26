from gurobipy import *
from gurobipy import GRB

def energyMain(nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, nodes):
    print("energyMain: " ,nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, nodes)

    communicationCost = solver.addVar(vtype=GRB.CONTINUOUS, name='communicationCost')
    communicationCostDown = solver.addVar(vtype=GRB.CONTINUOUS, name='communicationCostDown')
    computationCost = solver.addVar(vtype=GRB.CONTINUOUS, name='computationCost')
    communicationTime = solver.addVar(vtype=GRB.CONTINUOUS, name='communicationTime')
    computationTime = solver.addVar(vtype=GRB.CONTINUOUS, name='computationTime')
    cores = solver.addVar(vtype=GRB.INTEGER, name='cores')

    print()

    assignment = [[solver.addVar(vtype=GRB.BINARY, name="ASING_%s_%s" % (r, c)) for c in range(nNodes)]
                  for r in range(nTask * nUsers)]

    percentageCPU = [[solver.addVar(vtype=GRB.INTEGER, name="pCPU_%s_%s" % (r, c), lb=0,
                                    ub=cpuPercentages * nodes[r][14]) for c in range(nTask)]
                     for r in range(nNodes)]

    percentageCPUaux = [[solver.addVar(vtype=GRB.CONTINUOUS, name="auxPCPU_%s_%s" % (r, c), lb=0,
                                       ub=cpuPercentages * nodes[r][14]) for c in range(nTask)]
                        for r in range(nNodes)]

    constraints = [[0 for _ in range(nTask)] for _ in range(nConstraints)]
    return communicationCost, communicationCostDown, computationCost, communicationTime, computationTime, cores, assignment, percentageCPU, percentageCPUaux, constraints

if __name__ == "__main__":

    from imain import nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, nodes
    energyMain(nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, nodes)

    #Ejemplo energyMain:
    # energyMain(1,0,3,3,2, 
    # <gurobi.Model Continuous instance milp: 0 constrs, 0 vars, Parameter changes: NonConvex=2>, 
    # [[10000000, 150000000, 0.3, 75, 2000, 1, 0.7, 150000000, {''}, {''}, 'computing', 'class0', 'public', ['wlan'], 2, 30.0, 0.01], [10000000, 150000000, 0.3, 75, 2000, 1, 0.7, 150000000, {''}, {''}, 'computing', 'class1', 'public', ['wlan'], 2, 30.0, 0.01], [10000000, 150000000, 0.3, 75, 2000, 1, 0.7, 150000000, {''}, {''}, 'computing', 'class2', 'public', ['wlan'], 2, 30.0, 0.01]])