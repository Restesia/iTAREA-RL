import sys
import json
import subprocess
from gurobipy import *

nUsers = None
nConstraints = None
nTask = None
nNodes = None
cpuPercentages = None
tasks = None
nodes = None
relation = None
rtt = None



###
### Método que crea el problema: principalmente definimos la matriz de tareas y de nodos con sus características.
###
def set_problem_size ():
	global nUsers
	global nConstraints
	global nTask
	global nNodes
	global cpuPercentages
	global tasks
	global nodes

	nTask = len(tasks_list) # Number of tasks
	nNodes = len(nodes_list) # Number of nodes that form the infrastructure

	nUsers = 1 #1 (by default) in case of executing the iTAREA module each time a new user join the network.
	nConstraints = 0 #Number of application's time constraints
	cpuPercentages = 2 # Granularity of the core partitions assigned (1/cpuPercentages). e.g., portions of 500 milicores in case of cpuPercentages=2

	
	tasks = [ [ 0 for c in range(11) ] 
      	for r in range(int(nTask)) ]

	nodes = [ [ 0 for c in range(17) ] 
	      for r in range(int(nNodes)) ]

###
### Este método crea una matriz con los datos que se intercambian entre las tareas, 
### es decir, para la casilla i,j el valor es X, la tarea i manda X bits a la tarea J 
###
def set_data_to_transmit ():
	global relation
	# Data to be transmitted between tasks (bits)
	relation = [ [ 0 for c in range(nTask) ] 
		      for r in range(nTask) ]

	#Example: task 0 sends to task 1 1000 bits
      #relation[0][1] = 1000

###
### Matriz placeholder de tareas
### Si se quisiera implementar de forma real con planetarium este método de alguna forma tendría que recoger los datos de las tareas
### y debería aquí realizarse la creación de la matriz con el número de tareas a asignar
###
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
		for x, task in enumerate(tasks_list):
			task_data = [
				int(task['cpucycles']),
				int(task['ram']),
				int(task['user']),
				int(task['mintransm']),
				list(eval(task['sensreq'])),  # Convertir el conjunto en una lista utilizando eval()
				list(eval(task['periphreq'])),  # Convertir el conjunto en una lista utilizando eval()
				list(eval(task['transmit'])),  # Convertir el conjunto en una lista utilizando eval()
				task['exlocation'],
				task['tasktype'],
				int(task['disk']),
				task['taskname']
			]
			tasks.append(task_data)


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

	for x, node in enumerate(nodes_list):
		node = [
            int(node['cpu']),
            int(node['bwup']),
            float(node['pwup']),
            int(node['maxenergy']),
            int(node['ram']),
            float(node['importance']),
            float(node['pwdown']),
            int(node['bwdown']),
            list(eval(node['sensingunits'])),  # Convertir el conjunto en una lista utilizando eval()
            list(eval(node['peripherials'])),  # Convertir el conjunto en una lista utilizando eval()
            list(eval(node['typecore'])),  # Convertir el conjunto en una lista utilizando eval()
            eval(node['location']),
            node['owner'],
            list(eval(node['comcap'])),  # Convertir el conjunto en una lista utilizando eval()
            int(node['cores']),
            float(node['percnormal']),
            float(node['percsleeping'])
		]
	nodes.append(node)


def printAll():
    print("-nUsers:", nUsers)
    print("-nConstraints:", nConstraints)
    print("-nTask:", nTask)
    print("-nNodes:", nNodes)
    print("-cpuPercentages:", cpuPercentages)
    print("-tasks:", tasks) #VACÍO
    print("-nodes:", nodes) #VACÍO
    print("-relation:", relation)  #VACÍO
    print("-rtt:", rtt) 

def callSolver():
	
	nlist = json.dumps(nodes_list)
	tlist = json.dumps(tasks_list)
	relation_str = json.dumps(relation)
	rtt_str = json.dumps(rtt)

	print("*nlist", nlist) 
	print("*tlist", tlist) 

	cmd = ['python', 'app/isolver.py', str(nUsers), str(nConstraints), str(nTask), str(nNodes), str(cpuPercentages), nlist, tlist, relation_str, rtt_str]
	output = subprocess.check_output(cmd).decode('utf-8')
	return output
		

if __name__ == "__main__":

	# Obtener los argumentos pasados desde app.py
	json_nodes_list = sys.argv[1] 
	json_tasks_list = sys.argv[2] 

	# Convertir los datos JSON a listas de Python
	nodes_list = json.loads(json_nodes_list)
	tasks_list = json.loads(json_tasks_list)	

	set_problem_size ()
	set_data_to_transmit ()
	set_nodes ()	
	set_tasks ()
	set_rtt ()
	
	callSolver()

	print() # Esta salida será capturada por app.py en el futuro