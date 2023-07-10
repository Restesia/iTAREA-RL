from kubernetes import client, config

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
	    print("  Dirección IP: %s" % node.status.addresses[0].address)
	    print("  Estado: %s" % node.status.conditions[0].type)
	    print("")

	# Obtener la lista de servicios en el clúster
	print("Servicios en el clúster de Kubernetes:")
	services = v1.list_service_for_all_namespaces().items
	for service in services:
	    print("- Nombre: %s" % service.metadata.name)
	    print("  Namespace: %s" % service.metadata.namespace)
	    print("  Tipo: %s" % service.spec.type)
	    print("  Puertos expuestos: %s" % service.spec.ports)
	    print("")


if __name__ == "__main__":
    print_info()
