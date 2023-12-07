import Tensorflow

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
	
	print()
	print("communicationCost: ", communicationCost.X)
	print("communicationCostDown: ", communicationCostDown.X)
	print("computationCost: ", computationCost.X)
	print("communicationTime: ", communicationTime.X)
	print("computationTime: ", computationTime.X)
	print("cores: ", cores.X)
	print()

if __name__ == "__main__":

	set_problem_size ()
	set_data_to_transmit ()
	set_nodes ()
	set_tasks ()
	set_rtt ()
	solve ()
