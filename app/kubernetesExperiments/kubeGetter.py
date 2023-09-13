from kubernetes import client, config

# CONSUMO ENERGÍA (WATTS)
#import hardware_monitoring_library
# power_consumption = hardware_monitoring_library.get_power_consumption()

# Cargar la configuración del archivo kubeconfig (o usar la configuración por defecto)
config.load_kube_config()
print(config.load_kube_config())

# Crear una instancia del objeto API de Kubernetes
v1 = client.CoreV1Api()
custom_api = client.CustomObjectsApi()


def print_info():
	print("-Finish-")
	nodes = v1.list_node().items
	for node in nodes:
		print("- Nombre: %s" % node.metadata.name)
		

	# Obtener la lista de servicios en el clúster
	print("Pods en el clúster de Kubernetes:")
	pods = v1.list_namespaced_pod("default").items
	for pod in pods:
		print("- Nombre: %s" % pod.metadata.name)
		print("  Namespace: %s" % pod.metadata.namespace)
	#	print("  Tipo: %s" % pod.spec.type)
	#	print("  Puertos expuestos: %s" % pod.spec.ports)
	#	print("")


if __name__ == "__main__":
    print_info()
