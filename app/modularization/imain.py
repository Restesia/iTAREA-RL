from isetter import * 
from ienergy import *
from isolver import *
from iprinter import *

if __name__ == "__main__":
    
    # 1. Obtener los valores
    nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt = setterMain()

    # 2. Conseguir energía
    communicationCost, communicationCostDown, computationCost, communicationTime, computationTime, cores, assignment, percentageCPU, percentageCPUaux, constraints = energyMain(nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, nodes)
    
    # 3. Llamar a la función solveAll
    solver = solverMain(
        tasks, 
        nodes, 
        relation, 
        rtt, 
        nUsers, 
        nConstraints, 
        nTask, 
        nNodes, 
        cpuPercentages, 
        solver, 
        communicationCost, 
        communicationCostDown, 
        computationCost, 
        communicationTime, 
        computationTime, 
        cores, 
        assignment, 
        percentageCPU, 
        percentageCPUaux, 
        constraints)

    # 4. Imprimir
    printerMain(cpuPercentages, solver)