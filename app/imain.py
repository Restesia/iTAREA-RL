from isetter import *
from ienergy import *
from isolver import *
from iprinter import *

import sys
import json
res=""

nodes_list=""
tasks_list=""

# Convertir los datos JSON a listas de Python
def getLists(json_nodes_list , json_tasks_list):
 
    nodes_list = json.loads(json_nodes_list)
    tasks_list = json.loads(json_tasks_list)
    return nodes_list,tasks_list

def convertListsToSetsFromMap(myList):
    for i in range(len(myList)):
        if isinstance(myList[i], list):
            myList[i] = set(myList[i])
    return myList

if __name__ == "__main__":

    # 1. Rescatar las listas
    nodes_list, tasks_list = getLists(sys.argv[1], sys.argv[2])
    nodes_list = convertListsToSetsFromMap(nodes_list)
    tasks_list = convertListsToSetsFromMap(tasks_list)
    #res = "NODES: " + str(nodes_list) + "\nTASKS: " + str(tasks_list) + "\n"  + "\n"
    
    # 2. Obtener los valores
    nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, tasks, nodes, relation, rtt = setterMain(nodes_list, tasks_list)
    #res += "USERS: " + str(nUsers) + "\n" + "CONSTRAINTS: " + str(nConstraints) + "\n" + "NUMBER OF TASKS: " + str(nTask) + "\n" + "NUMBER OF NODES: " + str(nNodes) + "\n" + "CPU PERCENTAGES: " + str(cpuPercentages) + "\n" + "SOLVER: " +  str(solver) + "\n" + "TASKS: " + str(tasks) + "\n" + "NODES: " + str(nodes) + "\n" + "RELATION: " + str(relation) + "\n" + "RTT: " + str(rtt) + "\n" + "\n"
    

    #--------------------------------------------------
    
    # 3. Conseguir energía
    communicationCost, communicationCostDown, computationCost, communicationTime, computationTime, cores, assignment, percentageCPU, percentageCPUaux, constraints = energyMain(nUsers, nConstraints, nTask, nNodes, cpuPercentages, solver, nodes)
    #res += "COMMUNICATION COST: " + str(communicationCost) + "\n" + "COMMUNICATION COST DOWN: " + str(communicationCostDown) + "\n" + "COMPUTATION COST: " + str(computationCost) + "\n" + "COMMUNICATION TIME: " + str(communicationTime) + "\n" + "COMPUTATION TIME: " + str(computationTime) + "\n" + "CORES: " + str(cores) + "\n" + "ASSIGNMENT: " + str(assignment) + "\n" + "PERCENTAGE CPU: " + str(percentageCPU) + "\n" + "PERCENTAGE CPU AUX: " + str(percentageCPUaux) + "\n" + "CONSTRAINTS: " + str(constraints) + "\n"
    
    print("communicationCost: ", communicationCost)
    print("communicationCostDown: ", communicationCostDown)
    print("computationCost: ", computationCost)
    print("communicationTime: ", communicationTime)
    print("computationTime: ", computationTime)
    print("cores: ", cores)


    # 4. Llamar a la función solveAll
    solver = solverMain(
        tasks, 
        nodes, 
        relation, 
        rtt, 
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

    
    # 4. Imprimir pantalla
    res += str(printerMain(cpuPercentages, solver))
    #res += "NODES: " + str(nodes_list) + "\n"
    #res += "TASKS: " + str(tasks_list) + "\n"