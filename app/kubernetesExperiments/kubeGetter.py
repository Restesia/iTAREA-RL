from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
custom_api = client.CustomObjectsApi()

def get_cpu_clock_speed():
    try:
        with open('/proc/cpuinfo', 'r') as file:
            lines = file.readlines()
        for line in lines:
            if 'MHz' in line:
                clock_speed_mhz = float(line.split(':')[1].strip())
                return clock_speed_mhz
    except Exception as e:
        print("Error al obtener la frecuencia del reloj de la CPU:", str(e))
    return None

def get_bandwidth_up(node_name):
    try:
        node = v1.read_node(node_name)
        bandwidth_up = node.metadata.annotations.get("projectcalico.org/IPv4Address")
        print("NODE: ", node.metadata.annotations)
        return bandwidth_up
    except Exception as e:
        print("Error al obtener la capacidad de Bandwidth up:", str(e))

def print_info():
    print("-Finish-")
    nodes = v1.list_node().items
    pods = v1.list_namespaced_pod("default").items
    
    for node in nodes:
       
	    #GET DATA
        node_name = node.metadata.name
        cpu_capacity_milicores = node.status.capacity["cpu"]
        clock_speed = get_cpu_clock_speed() * 1e6 # Hz (MHz = 1e6 Hz)
        ram_mb = (int(node.status.capacity.get("memory")[:-2]) / 1024 ) * 1000
        cpu_capacity_cps = float(cpu_capacity_milicores) * clock_speed
        #bandwidth_up = get_bandwidth_up(node_name)  
        #power_consumption = hardware_monitoring_library.get_power_consumption()
        
		#PRINTS
        print("- Nombre: %s" % node_name)
        print("  Number of cores: %s" % cpu_capacity_milicores)
        print("  RAM (MB): %s" % ram_mb)
        print("  Capacidad de CPU en ciclos por segundo: %s" % cpu_capacity_cps)
        #print("  Bandwidth up (bits/s) : %s" % bandwidth_up)
        

    print("Pods en el clúster de Kubernetes:")
    for pod in pods: 
        print("- Nombre: %s" % pod.metadata.name)
		
	#	print("  Namespace: %s" % pod.metadata.namespace)
	#	print("  Tipo: %s" % pod.spec.type)
	#	print("  Puertos expuestos: %s" % pod.spec.ports)


if __name__ == "__main__":
    print_info()
