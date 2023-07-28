from gurobipy import *
import re

#SOLVER.STATUS
#LOADED	    1	Model is loaded, but no solution information is available.
#OPTIMAL	2	Model was solved to optimality (subject to tolerances), and an optimal solution is available.
#INFEASIBLE	3	Model was proven to be infeasible.

def printerMain(cpuPercentages, solver):
    print("solver.status: ",solver.status, "(",solver.status!=3,")")
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