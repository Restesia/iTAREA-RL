from gurobipy import *
from gurobipy import Model, GRB, quicksum, re
nUsers = None
nConstraints = None
nTask = None
nNodes = None
cpuPercentages = None
solver = None
tasks = None
nodes = None
relation = None
rtt = None

### Método que crea el problema: principalmente definimos la matriz de tareas y de nodos con sus características.
def set_problem_size ():
	global nUsers
	global nConstraints
	global nTask
	global nNodes
	global cpuPercentages
	global solver
	global tasks
	global nodes

	nUsers = 1 #1 (by default) in case of executing the iTAREA module each time a new user join the network.
	nConstraints = 0 #Number of application's time constraints
	nTask = 5 # Number of tasks
	nNodes = 5 # Number of nodes that form the infrastructure
	cpuPercentages = 2 # Granularity of the core partitions assigned (1/cpuPercentages). e.g., portions of 500 milicores in case of cpuPercentages=2
	solver = Model("milp") # Kind of solver used by Gurobi to obtain the solution (depends on the problem)
	solver.setParam(GRB.Param.NonConvex, 2) # Parameter to configure Gubori to solve the iTAREA
	
	tasks = [ [ 0 for c in range(11) ] 
      	for r in range(nTask) ]

	nodes = [ [ 0 for c in range(17) ] 
	      for r in range(nNodes) ]


### Este método crea una matriz con los datos que se intercambian entre las tareas, 
### es decir, para la casilla i,j el valor es X, la tarea i manda X bits a la tarea J 
def set_data_to_transmit ():
	global relation
	# Data to be transmitted between tasks (bits)
	relation = [ [ 0 for c in range(nTask) ] 
		      for r in range(nTask) ]

	#Example: task 0 sends to task 1 1000 bits
      #relation[0][1] = 1000

### Matriz placeholder de tareas
### Si se quisiera implementar de forma real con planetarium este método de alguna forma tendría que recoger los datos de las tareas
### y debería aquí realizarse la creación de la matriz con el número de tareas a asignar
def set_tasks () :
# Defining each task that forms the application:

# 0 - CPU cycles, 
# 1 - RAM required (mb), 
# 2 - User (in case of replication for multiple users, 0 by default), 
# 3 - Minimal transmission (in case of requiring a minimal bandwidtk (e.g., for video streaming in a specific quality)), 
# 4 - Sensing requirements (e.g., thermometer), 
# 5 - Peripheral requirements (e.g., camera, GPU), 
# 6 - Transmit
# 7 - Exact location (in case the app is located in a specific place (e.g., dispatch 4.1) 'none' by default), 
# 8 - Type (e.g., sensing mote)
# 9 - Disk required (Mb) 
# 10 - Task name

	for x in range(nTask):
		tasks[x][0] = 150000
		tasks[x][1] = 150
		tasks[x][2] = 0
		tasks[x][3] = 0
		tasks[x][4] = {''}
		tasks[x][5] = {''}
		tasks[x][6] = {}
		tasks[x][7] = 'none'
		tasks[x][8] = 'computing'
		tasks[x][9] = 100
		tasks[x][10] = 'name'

### Método que asigna el rtt, para conseguir el objetivo de reducir latencia
def set_rtt ():

	# Round trip time (s) between nodes. e.g., RTT between node 0 and 1: rtt[0][1]
	rtt = [ [ 0.01 for c in range(nNodes) ] 
			for r in range(nNodes) ]

### Método análogo al de las tareas, habría que conseguir que en este se crearan los nodos en base 
### al número de nodos y sus características dentro del clúster de kubernetes
def set_nodes ():

# Defining each node that forms the infrastructure

# 0 - CPU (cycles per second)
# 1 - Bandwidth up (bits/s)
# 2 - Power Upload (Ptx), 
# 3 - Maximum energy consumption (Watts) 
# 4 - RAM (Mb)
# 5 - Importance of saving energy in nodes (real number between 0 and 1). In this case, all nodes has been configured with the same node weighting (1) 
# 6 - Power Download (Prx), 
# 7 - Bandwidth Down (bits/s), 
# 8 - Sensing units (e.g., thermomether), '' if any 
# 9 - Peripherals (e.g., GPU), '' if any
# 10 - Type (e.g., sensing mote), 'computing' by default
# 11- Location (e.g., dispatch 2.30),  
# 12 - Owner (e,g., CAOSD group), 'public' by default
# 13 - Communication capacities (e.g., wlan)
# 14 - Number of cores, 
# 15 - Percentage of idle energy consumption, 
# 16 - Percentage of energy consumption in sleeping mode

	for x in range(0, nNodes):
		nodes[x][0] = 10000000
		nodes[x][1] = 150000000
		nodes[x][2] = 0.3
		nodes[x][3] = 75
		nodes[x][4] = 2000
		nodes[x][5] = 1
		nodes[x][6] = 0.7
		nodes[x][7] = 150000000
		nodes[x][8] = {''}
		nodes[x][9] = {''}
		nodes[x][10] = 'computing'
		nodes[x][11] = 'class'+str(x)
		# nodes[x][12] = 'public'
		# nodes[x][13] = {'wlan'}
		nodes[x][14] = 2
		nodes[x][15] = 30
		# nodes[x][16] = 0.01

### Este método es el más importante, hace uso de la sintaxis de gurobi para plantear el problema de optimización
def solve ():
	# Defining problem variables to optimize

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

	##### NOTA: La integración del modelo de aprendizaje automático predictor de energía se realizaría aquí
	##### Los costes de computación y comunicación en vez de utilizar la fórmula especificada, se convertirían en una llamada al modelo de predicción.
	##### Deberíamos tener una matriz con el consumo de las n tareas en los m nodos, para poder calcular el mínimo

	for c in range(nConstraints):

		solver.addConstr( communicationTime == quicksum(quicksum(quicksum(assignment[constraints[c][i]][m]*(1-assignment[constraints[c][j]][m])*(((relation[constraints[c][i]][constraints[c][j]]*1000000)/nodes[m][1])+(rtt[0][0]*1000000)) for j in range(2, 2 + constraints[c][1]))  for i in range(2, 2 + constraints[c][1]))  for m in range(nNodes)))
		solver.addConstr( computationTime == quicksum(quicksum((assignment[constraints[c][i]][m]*((tasks[constraints[c][i]][0]*1000000)*(percentageCPUaux[m][constraints[c][i]])*nodes[m][14]*cpuPercentages))/nodes[m][0] for i in range(2, 2 + constraints[c][1]))  for m in range(nNodes)))
		solver.addConstr( (computationTime + communicationTime) <= (constraints[c][0]*1000000))


	##### Sería cambiar estas 3 líneas por algo como
	##### totalCost == quicksum(quicksum(assignment[i][m]* calcularEnergía(i,m) for i in range(nTask)) for m in range (nNodes)))

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
				print('CPU assigned in Node ' + str(aux[0]) + ' to Task ' + str(aux[1]) + '. CPU (cores): ' + str(int(v.x)/(cpuPercentages)))
	else:
		print('The model is infeasible')

if __name__ == "__main__":

	set_problem_size ()
	set_data_to_transmit ()
	set_nodes ()
	set_tasks ()
	set_rtt ()
	solve ()