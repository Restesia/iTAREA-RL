from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
custom_api = client.CustomObjectsApi()

def get_node_cpu_clock_speed():
    try:
        with open('/proc/cpuinfo', 'r') as file:
            lines = file.readlines()
        for line in lines:
            if 'MHz' in line:
                clock_speed_mhz = float(line.split(':')[1].strip())
                return clock_speed_mhz * 1e6 # Hz (MHz = 1e6 Hz)
    except Exception as e:
        print("Error al obtener la frecuencia del reloj de la CPU:", str(e))
    return None

def get_node_bandwidth_up(node_name):
    try:
        node = v1.read_node(node_name)
        bandwidth_up = node.metadata.annotations.get("projectcalico.org/IPv4Address")
        print("NODE: ", node.metadata.annotations)
        return bandwidth_up
    except Exception as e:
        print("Error al obtener la capacidad de Bandwidth up:", str(e))

def get_node_power_upload(node_name): # -FOR TESTING-
    try:
        node = v1.read_node(node_name)
        power_upload = node.metadata.annotations.get("power_upload")
        return power_upload
    except Exception as e:
        print("Error al obtener la capacidad de carga de energía:", str(e))
        return None


def get_node_power_download(node_name):
    try:
        node = v1.read_node(node_name)
        power_download = node.metadata.annotations.get("power_download")
        return power_download
    except Exception as e:
        print("Error al obtener la capacidad de descarga de energía:", str(e))
        return None


def get_node_max_energy_consumption(node_name):
    try:
        node = v1.read_node(node_name)
        max_energy_consumption = node.metadata.annotations.get("max_energy_consumption")
        return max_energy_consumption
    except Exception as e:
        print("Error al obtener la máxima capacidad de consumo de energía:", str(e))
        return None

def get_node_type(node_name):
    try:
        node = v1.read_node(node_name)
        node_type = node.metadata.labels.get("tu.etiqueta.aqui")
        return node_type
    except Exception as e:
        print("Error al obtener el tipo de nodo:", str(e))
        return None


def get_pod_user(pod): # -FOR TESTING-
    return pod.spec.security_context.run_as_user

def get_pod_min_transmission(): # -FOR TESTING-
    return None

def get_pod_peripherial_requirements(): # -FOR TESTING-
    return None

def get_pod_exact_location(): # -FOR TESTING-
    return None

def get_pod_type(): # -FOR TESTING-
    return None

def print_info():

    print("-Finish-")
    nodes = v1.list_node().items
    pods = v1.list_namespaced_pod("default").items
    
    print("Nodes en el clúster de Kubernetes:")
    for node in nodes:
        
	    #GET NODE DATA
        node_name = node.metadata.name
        node_cpu_capacity_cps = float(node.status.capacity["cpu"]) * get_node_cpu_clock_speed()
        node_power_upload = get_node_power_upload(node_name)
        node_power_download = get_node_power_download(node_name) 
        node_max_energy_consumption = get_node_max_energy_consumption(node_name)
        node_type = get_node_type(node_name) 
        #bandwidth_up = get_bandwidth_up(node_name)  
        #power_consumption = hardware_monitoring_library.get_power_consumption()
        #ram_mb = (int(node.status.capacity.get("memory")[:-2]) / 1024 ) * 1000

		#PRINTS NODE
        print("- Nombre: %s" % node_name)
        print("  Capacidad de CPU en ciclos por segundo: %s" % node_cpu_capacity_cps)
        print("  Nombre: %s" % node_power_upload)
        print("  Nombre: %s" % node_power_download)
        print("  Nombre: %s" % node_max_energy_consumption)
        print("  Nombre: %s" % node_type)
        #print("  Number of cores: %s" % cpu_capacity_milicores)
        #print("  RAM (MB): %s" % ram_mb)
        #print("  Bandwidth up (bits/s) : %s" % bandwidth_up)
        
    print("Pods en el clúster de Kubernetes:")
    for pod in pods: 

        #GET POD DATA
        pod_name = pod.metadata.name
        pod_user = get_pod_user(pod)
        pod_min_transmission = get_pod_min_transmission()
        pod_peripherial_requirements = get_pod_peripherial_requirements()
        pod_exact_location = get_pod_exact_location()
        pod_type = get_pod_type()

        #PRINTS POD
        print("- Nombre: %s" % pod_name)
        print("  User: %s" %   pod_user)
        print("  Minimal Transmission: %s" %   pod_min_transmission)
        print("  Peripherial Requirements: %s" %   pod_peripherial_requirements)
        print("  Exact location: %s" %   pod_exact_location)
        print("  Type: %s" %   pod_type)
        # print("  All: %s" % pod.metadata)
        # print("  Namespace: %s" % pod.metadata.namespace)
        # print("  Tipo: %s" % pod.spec.type)
        # print("  Puertos expuestos: %s" % pod.spec.ports)



if __name__ == "__main__":
    print_info()
