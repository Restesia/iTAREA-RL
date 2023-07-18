from isetter import * 
from isolver import *
from ienergy import *

if __name__ == "__main__":
    
    # 1. Obtener los valores
    nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt = getAll()

    # 2. Conseguir energía
    communicationCost, communicationCostDown, computationCost, communicationTime, computationTime, cores, assignment, percentageCPU, percentageCPUaux, constraints = getData(nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, nodes)
    
    # 3. Llamar a la función solveAll
    solveAll(tasks, nodes, relation, rtt, nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, communicationCost, communicationCostDown, computationCost, communicationTime, computationTime, cores, assignment, percentageCPU, percentageCPUaux, constraints)
