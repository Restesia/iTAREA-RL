from kubernetes import client, config

# Cargar la configuración del archivo kubeconfig (o usar la configuración por defecto)
config.load_kube_config()
print(config.load_kube_config())

# Crear una instancia del objeto API de Kubernetes
api = client.CoreV1Api()
custom_api = client.CustomObjectsApi()

def print_info():
	nodes = api.list_node().items
	for node in nodes:
	    print("- Nombre: %s" % node.metadata.name)
	    print("  Dirección IP: %s" % node.status.addresses[0].address)
	    print("  Estado: %s" % node.status.conditions[0].type)
	    print("")

	# Obtener la lista de servicios en el clúster
	print("Servicios en el clúster de Kubernetes:")
	services = api.list_service_for_all_namespaces().items
	for service in services:
	    print("- Nombre: %s" % service.metadata.name)
	    print("  Namespace: %s" % service.metadata.namespace)
	    print("  Tipo: %s" % service.spec.type)
	    print("  Puertos expuestos: %s" % service.spec.ports)
	    print("")

def get_cpu_usage_per_pod(pod):
    cpu_usage = 0
    
    if pod.status.phase == "Running":
        namespace = pod.metadata.namespace
        pod_name = pod.metadata.name
        
        #print(namespace)
        print(pod_name)

        try:
            metrics = custom_api.list_namespaced_custom_object(
                group="metrics.k8s.io",
                version="v1beta1",
                namespace=namespace,
                plural="pods",
                label_selector=f"pod-name={pod_name}"
            )

            if "items" in metrics and metrics["items"]:
                containers = metrics["items"][0]["containers"]

                for container in containers:
                    cpu_usage += container["usage"]["cpu"]
        except client.rest.ApiException as e:
            print(f"Exception when calling CustomObjectsApi: {e}")
    return cpu_usage

def get_bandwidth_per_usage_pod(pod):
    bandwidth_usage = 0

    if pod.status.phase == "Running":
        for container in pod.spec.containers:
            if container.resources.requests and 'network' in container.resources.requests:
                network_request = container.resources.requests['network']
                bandwidth_usage = convert_bandwidth_to_decimal(container.usage['network'])
                break

    return bandwidth_usage

def convert_cpu_to_decimal(cpu_string):
    # Convierte el uso de CPU en formato string a un valor decimal
    if cpu_string.endswith("n"):
        return float(cpu_string[:-1]) / 1000000000
    elif cpu_string.endswith("u"):
        return float(cpu_string[:-1]) / 1000000
    elif cpu_string.endswith("m"):
        return float(cpu_string[:-1]) / 1000
    else:
        return float(cpu_string)

def convert_bandwidth_to_decimal(bandwidth_string):
    # Convierte el uso de ancho de banda en formato string a un valor decimal
    if bandwidth_string.endswith("Ki"):
        return float(bandwidth_string[:-2]) / 1024
    elif bandwidth_string.endswith("Mi"):
        return float(bandwidth_string[:-2])
    elif bandwidth_string.endswith("Gi"):
        return float(bandwidth_string[:-2]) * 1024
    elif bandwidth_string.endswith("Ti"):
        return float(bandwidth_string[:-2]) * 1024 * 1024
    else:
        return float(bandwidth_string)

def get_cluster_cpu_usage():
    total_cpu_usage = 0

    # Obtener todos los pods en el cluster
    pods = api.list_pod_for_all_namespaces().items


    # Calcular el gasto de CPU total sumando el uso de CPU de cada pod
    for pod in pods:
        cpu_usage = get_cpu_usage_per_pod(pod)
        total_cpu_usage += cpu_usage

    return total_cpu_usage

def get_bandwidth_cluster():
    total_bandwidth_usage = 0

    # Obtener todos los pods en el cluster
    pods = api.list_pod_for_all_namespaces().items
    

    # Calcular el ancho de banda total sumando el uso de ancho de banda de cada pod
    for pod in pods:
        bandwidth_usage = get_bandwidth_usage_per_pod(pod)
        total_bandwidth_usage += bandwidth_usage

    return total_bandwidth_usage


if __name__ == "__main__":
	#print_info()
	cpu_usage = get_cluster_cpu_usage()
	#bandwidth_usage = get_bandwidth_cluster()

	print(f"Gasto de CPU del cluster: {cpu_usage}")
	#print(f"Gasto de ancho de banda del cluster: {bandwidth_usage}")
