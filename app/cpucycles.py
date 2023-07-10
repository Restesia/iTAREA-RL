#pip install psutil
import psutil
from kubernetes import client, config

def getGeneralMetrics():
    # Obtener el porcentaje de uso de la CPU
    cpu_percent = psutil.cpu_percent(interval=1)

    # Obtener el número de ciclos de CPU por segundo
    cpu_cycles = psutil.cpu_freq().current

    # Imprimir los resultados
    print("Porcentaje de uso de la CPU:", cpu_percent)
    print("Ciclos de CPU por segundo:", cpu_cycles)

def getTotalFromKubernetes(namespace):
    # Cargar la configuración del clúster desde el archivo kubeconfig
    config.load_kube_config()

    # Crear una instancia del cliente de Kubernetes
    api_instance = client.CoreV1Api()

    # Obtener la lista de pods en el namespace deseado
    pods = api_instance.list_namespaced_pod(namespace=namespace)

    total_cpu_usage = 0.0

    # Recorrer cada pod y obtener los ciclos de CPU
    for pod in pods.items:
        pod_name = pod.metadata.name

        # Obtener el nombre del contenedor principal del pod
        container_name = pod.spec.containers[0].name

        # Obtener el uso de CPU del contenedor
        response = api_instance.read_namespaced_pod(pod_name, namespace)
        cpu_usage = response.spec.containers[0].usage["cpu"]

        # Sumar el uso de CPU al total
        total_cpu_usage += float(cpu_usage.strip("n"))

    return total_cpu_usage

# Ejemplo de uso
# namespace = "mi-namespace"
# total_cpu = getTotalFromKubernetes(namespace)
# print("Total de uso de CPU en el clúster:", total_cpu)


def getPartialFromKubernetes(namespace):
    # Cargar la configuración del clúster desde el archivo kubeconfig
    config.load_kube_config()

    # Crear una instancia del cliente de Kubernetes
    api_instance = client.CoreV1Api()

    # Obtener la lista de pods en el namespace deseado
    pods = api_instance.list_namespaced_pod(namespace=namespace)

    total_cpu_usage = 0.0
    pod_cpu_usage = {}

    # Recorrer cada pod y obtener los ciclos de CPU
    for pod in pods.items:
        pod_name = pod.metadata.name

        # Obtener el nombre del contenedor principal del pod
        container_name = pod.spec.containers[0].name

        # Obtener el uso de CPU del contenedor
        response = api_instance.read_namespaced_pod(pod_name, namespace)
        cpu_usage = response.spec.containers[0].usage["cpu"]

        # Sumar el uso de CPU al total
        total_cpu_usage += float(cpu_usage.strip("n"))

        # Agregar el uso de CPU del pod al diccionario
        pod_cpu_usage[pod_name] = float(cpu_usage.strip("n"))

    # Obtener el consumo de CPU por nodo
    nodes = api_instance.list_node()
    node_cpu_usage = {}

    for node in nodes.items:
        node_name = node.metadata.name

        # Obtener la capacidad de CPU del nodo
        capacity = node.status.capacity
        cpu_capacity = float(capacity["cpu"])

        # Obtener el uso de CPU del nodo
        node_metrics = api_instance.read_node_metrics(node_name)
        cpu_usage = node_metrics.usage["cpu"]

        # Agregar el uso de CPU del nodo al diccionario
        node_cpu_usage[node_name] = {
            "usage": float(cpu_usage.strip("n")),
            "capacity": cpu_capacity
        }

    return total_cpu_usage, pod_cpu_usage, node_cpu_usage

# Ejemplo de uso
#namespace = "mi-namespace"
#total_cpu, pod_cpu, node_cpu = getTotalFromKubernetes(namespace)

#print("Total de uso de CPU en el clúster:", total_cpu)

#print("\nConsumo de CPU por pod:")
#for pod_name, cpu_usage in pod_cpu.items():
#    print(f"Pod: {pod_name} - Uso de CPU: {cpu_usage}")

#print("\nConsumo de CPU por nodo:")
#for node_name, cpu_info in node_cpu.items():
#    print(f"Nodo: {node_name}")
#    print(f"Uso de CPU: {cpu_info['usage']}")
#    print(f"Capacidad de CPU: {cpu_info['capacity']}")
#    print()

