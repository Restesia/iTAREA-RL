from gurobipy import *
import subprocess
import sys

solver = None

###
### Este método es el más importante, hace uso de la sintaxis de gurobi para plantear el problema de optimización
###
def solve ():

	# Defining problem variables to optimize
	global solver
	solver = Model("milp") # Kind of solver used by Gurobi to obtain the solution (depends on the problem)
	solver.setParam(GRB.Param.NonConvex, 2) # Parameter to configure Gubori to solve the iTAREA

	### especificamos las variables que va a tener el solver
	communicationCost = solver.addVar(vtype=GRB.CONTINUOUS, name='communicationCost')
	communicationCostDown = solver.addVar(vtype=GRB.CONTINUOUS, name='communicationCostDown')
	computationCost = solver.addVar(vtype=GRB.CONTINUOUS, name='computationCost')
	communicationTime = solver.addVar(vtype=GRB.CONTINUOUS, name='communicationTime')
	computationTime = solver.addVar(vtype=GRB.CONTINUOUS, name='computationTime')
	cores = solver.addVar(vtype=GRB.INTEGER, name='cores')

	### matriz con la soluciones del asignado
	assignment = [ [ solver.addVar(vtype=GRB.BINARY, name="ASING_%s_%s" % (r,c)) for c in range(nNodes) ] 
		for r in range(nTask*nUsers) ]

	# {node, % core assigned to task}
	percentageCPU = [ [ solver.addVar(vtype=GRB.INTEGER, name="pCPU_%s_%s" % (r,c), lb=0, ub=cpuPercentages*nodes[r][14]) for c in range(nTask) ] for r in range(nNodes) ]

	# {node, % core assigned to task} This variable is used to avoid the division between variables (not supported by default)
	percentageCPUaux = [ [ solver.addVar(vtype=GRB.CONTINUOUS, name="auxPCPU_%s_%s" % (r,c), lb=0, ub=cpuPercentages*nodes[r][14]) for c in range(nTask) ] for r in range(nNodes) ]

	# Edges of the task-call graph
	constraints = [ [ 0 for c in range(nTask) ] for r in range(nConstraints) ]


	# Defining the time constratins (to assure the QoS).

	# 0 - max time to be executed
	# 1 - Number of tasks involved in the time constraint
	# 2...n - Index of the involved tasks
	# Example of time constraint. Max time, 0.5 seg. 3 tasks involved (0,1,2).

		# constraints[0][0] = 0.5
		# constraints[0][1] = 3
		# constraints[0][2] = 0
		# constraints[0][3] = 1
		# constraints[0][4] = 2

	### Añadimos algunas restricciones como que el porcentaje de cpu no supere el máximo
	for t in range(nTask): 
		solver.addConstr(quicksum(assignment[t][n] for n in range(nNodes)) == 1)

		for n in range(nNodes):
			solver.addConstr(((assignment [t][n])*(tasks[t][4] <= nodes[n][8]) * (tasks[t][5] <= nodes[n][9]) * (tasks[t][3] <= nodes[n][1]) * (tasks[t][8] == nodes[n][10]) * ((tasks[t][7] == 'none') + (tasks[t][7] == nodes[n][11])) == assignment[t][n]))
			solver.addConstr(percentageCPU[n][t] == percentageCPU[n][t]*assignment[t][n])

	for n in range(nNodes):

		for t in range(nTask):

			solver.addConstr((percentageCPU[n][t]*percentageCPUaux[n][t]) == assignment[t][n])

	for m in range(nNodes):

		solver.addConstr(quicksum(percentageCPU[m]) <= cpuPercentages*nodes[m][14])
		solver.addConstr(quicksum(assignment[t][m] * tasks[t][1] for t in range(nTask)) <= nodes[m][4]) #Checking RAM

	### Especificamos las fórmulas para calcular los tiempos y costes energéticos de comunicación y computación

	#####
	#####
	##### NOTA: La integración del modelo de aprendizaje automático predictor de energía se realizaría aquí
	##### Los costes de computación y comunicación en vez de utilizar la fórmula especificada, se convertirían en una llamada al modelo de predicción.
	##### Deberíamos tener una matriz con el consumo de las n tareas en los m nodos, para poder calcular el mínimo
	#####
	#####
	for c in range(nConstraints):

		solver.addConstr( communicationTime == quicksum(quicksum(quicksum(assignment[constraints[c][i]][m]*(1-assignment[constraints[c][j]][m])*(((relation[constraints[c][i]][constraints[c][j]]*1000000)/nodes[m][1])+(rtt[0][0]*1000000)) for j in range(2, 2 + constraints[c][1]))  for i in range(2, 2 + constraints[c][1]))  for m in range(nNodes)))
		solver.addConstr( computationTime == quicksum(quicksum((assignment[constraints[c][i]][m]*((tasks[constraints[c][i]][0]*1000000)*(percentageCPUaux[m][constraints[c][i]])*nodes[m][14]*cpuPercentages))/nodes[m][0] for i in range(2, 2 + constraints[c][1]))  for m in range(nNodes)))
		solver.addConstr( (computationTime + communicationTime) <= (constraints[c][0]*1000000))

	#####
	#####
	##### Sería cambiar estas 3 líneas por algo como
	##### totalCost == quicksum(quicksum(assignment[i][m]* calcularEnergía(i,m) for i in range(nTask)) for m in range (nNodes)))
	#####

	solver.addConstr(communicationCost ==  quicksum(quicksum(quicksum(assignment[i][m]*(1-assignment[j][m])*(nodes[m][2]*(relation[i][j]/nodes[m][1])*nodes[m][5]) for j in range(nTask)) for i in range(nTask)) for m in range(nNodes)))
	solver.addConstr(computationCost ==  quicksum(quicksum(assignment[i][m]*((100-nodes[m][15])/100) * nodes[m][3] * ((tasks[i][0]*10000)/nodes[m][0]) for i in range(nTask)) for m in range (nNodes)))
	solver.addConstr(communicationCostDown ==  quicksum(quicksum(quicksum(assignment[i][m]*(1-assignment[j][m])*(nodes[m][6]*(relation[j][i]/nodes[m][7])*nodes[m][5]) for j in range(nTask)) for i in range(nTask)) for m in range(nNodes)))

	solver.addConstr(cores == quicksum(quicksum(percentageCPU[m][t] for t in range(nTask)) for m in range(nNodes)))

	### Establecemos los objetivos de minimización
	solver.setObjectiveN(communicationCost + communicationCostDown + computationCost, 0, GRB.MINIMIZE)
	solver.setObjectiveN(cores, 1, GRB.MINIMIZE)

	solver.optimize()

	###comprobamos que se encuentre solución y la imprimimos por pantalla
	###SERÍA NECESARIO ADAPTAR LA SALIDA A UN FORMATO QUE PUDIERA LEER PLANETARIUM
	if solver.status != 3:
		for v in solver.getVars():
			if v.varName[0:5] == 'ASING' and v.x == 1:
				aux = re.findall('\d+', v.varName)
				print('Task ' + str(aux[0]) + ' assigned to Node ' + str(aux[1]))

			if str(v.varName[0:4]) == 'pCPU' and v.x > 0:
				aux = re.findall('\d+', v.varName)
				result +='CPU assigned in Node ' + str(aux[0]) + ' to Task ' + str(aux[1]) + '. CPU (cores): ' + str(int(v.x)/(cpuPercentages)) + '\n'
	else:
		result = 'The model is infeasible'
	return result

if __name__ == "__main__":
    
	#cmd = ['python', 'app\\iTarea-solver.py', 
	# 1 str(nUsers), 
	# 2 str(nConstraints), 
	# str(nTask), str(nNodes), 5 str(cpuPercentages), 6 nodes, 7 tasks]
    
    nUsers = sys.argv[1]  # Argumento 2 (nUsers)
    nConstraints_arg = sys.argv[2]  # Argumento 3 (nConstraints)
    nTask_arg = sys.argv[3]  # Argumento 4 (nTask)
    nNodes_arg = sys.argv[4]  # Argumento 5 (nNodes)
    cpuPercentages_arg = sys.argv[5]  # Argumento 6 (cpuPercentages)
    nodes = sys.argv[6] 
    tasks = sys.argv[6] 

    # Convertir los argumentos de cadena a su tipo original
    nUsers = int(nUsers)
    nConstraints = int(nConstraints_arg)
    nTask = int(nTask_arg)
    nNodes = int(nNodes_arg)
    cpuPercentages = int(cpuPercentages_arg)
    
	#Resultado
    result = solve() 
    print(result)