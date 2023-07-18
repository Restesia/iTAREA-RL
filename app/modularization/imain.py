from isetter import *
from ienergy import *
from isolver import *
from iprinter import *

import sys
import json


def getLists():
    json_nodes_list = sys.argv[1]
    json_tasks_list = sys.argv[2]
 
    # Convertir los datos JSON a listas de Python
    nodes_list = json.loads(json_nodes_list)
    tasks_list = json.loads(json_tasks_list)
    return nodes_list,tasks_list

if __name__ == "__main__":

    nodes_list, tasks_list = getLists(sys.argv[1], sys.argv[2])

    # Realizar cualquier procesamiento necesario con nodes_list y tasks_list
    result = "El resultado que deseas devolver como un string"

    # Imprimir el resultado en lugar de utilizar print
    print(result)


    #--------------------------------------------------
    
    # 1. Obtener los valores
    #nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt = setterMain(nodes_list, tasks_list)

    # 2. Conseguir energía
    #communicationCost, communicationCostDown, computationCost, communicationTime, computationTime, cores, assignment, percentageCPU, percentageCPUaux, constraints = energyMain(nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, nodes)
    
    # 3. Llamar a la función solveAll
    # solver = solverMain(
    #     tasks, 
    #     nodes, 
    #     relation, 
    #     rtt, 
    #     nUsers, 
    #     nConstraints, 
    #     nTask, 
    #     nNodes, 
    #     cpuPercentages, 
    #     solver, 
    #     communicationCost, 
    #     communicationCostDown, 
    #     computationCost, 
    #     communicationTime, 
    #     computationTime, 
    #     cores, 
    #     assignment, 
    #     percentageCPU, 
    #     percentageCPUaux, 
    #     constraints)

    # 4. Imprimir
    # printerMain(cpuPercentages, solver)