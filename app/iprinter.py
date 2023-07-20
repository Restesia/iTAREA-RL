from gurobipy import *
import re

def printerMain(cpuPercentages, solver):
    print("")
    if solver.status != 3:
        for v in solver.getVars():
            if v.varName[0:5] == 'ASING' and v.x == 1:
                aux = re.findall('\d+', v.varName)
                print('Task ' + str(aux[0]) + ' assigned to Node ' + str(aux[1]))

            if str(v.varName[0:4]) == 'pCPU' and v.x > 0:
                aux = re.findall('\d+', v.varName)
                print('CPU assigned in Node ' + str(aux[0]) + ' to Task ' + str(aux[1]) +
                      '. CPU (cores): ' + str(int(v.x) / (cpuPercentages)))
    else:
        print('The model is infeasible')

if __name__ == "__main__":
    printerMain(cpuPercentages, solver)