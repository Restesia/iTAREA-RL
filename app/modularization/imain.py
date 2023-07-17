from isetter import *
from isolver import *

if __name__ == "__main__":
    
    # 1. Obtener los valores
    nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt = getAll()

    # 2. Llamar a la función solveAll
    solveAll(solve, printAssignment, getData, nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt)
