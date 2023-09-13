from kubernetes import client, config
import subprocess

# CONSUMO ENERGÍA (WATTS)
#import hardware_monitoring_library
# power_consumption = hardware_monitoring_library.get_power_consumption()

# Cargar la configuración del archivo kubeconfig (o usar la configuración por defecto)
config.load_kube_config()
print(config.load_kube_config())

# Crear una instancia del objeto API de Kubernetes
v1 = client.CoreV1Api()
custom_api = client.CustomObjectsApi()

def get_cpu_clock_speed():
    try:
        result = subprocess.run(['lscpu', '--parse=MHz'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("RESULT: ",result.returncode)
        if result.returncode == 0:
            output = result.stdout.decode('utf-8')
            lines = output.strip().split('\n')
           
		    # La frecuencia del reloj de la CPU puede estar en la primera línea (primer núcleo).
            if lines:
                clock_speed_mhz = float(lines[0])
                return clock_speed_mhz
    except Exception as e:
        print("Error al obtener la frecuencia del reloj de la CPU:", str(e))
    
    return None


def print_info():
    print("-Finish-")
    nodes = v1.list_node().items
    pods = v1.list_namespaced_pod("default").items
    
    for node in nodes:
       
	    #GET DATA
        cpu_capacity_milicores = node.status.capacity["cpu"]
        clock_speed = get_cpu_clock_speed()
        ram_mb = (int(node.status.capacity.get("memory")[:-2]) / 1024 ) * 1000
        
		#PRINTS
        print("- Nombre: %s" % node.metadata.name)
        print("  Number of cores: %s" % cpu_capacity_milicores)
        print("  RAM (MB): %s" % ram_mb)
        print("  Frecuencia del reloj de la CPU (MHz): %s" % clock_speed)
    print("Pods en el clúster de Kubernetes:")
    for pod in pods: 
        print("- Nombre: %s" % pod.metadata.name)
		
	#	print("  Namespace: %s" % pod.metadata.namespace)
	#	print("  Tipo: %s" % pod.spec.type)
	#	print("  Puertos expuestos: %s" % pod.spec.ports)


if __name__ == "__main__":
    print_info()
