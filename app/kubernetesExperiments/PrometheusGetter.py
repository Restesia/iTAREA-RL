from prometheus_api_client import PrometheusConnect

# Conecta con el servidor Prometheus
prom = PrometheusConnect(url="http://localhost:30000")

# Define la consulta para obtener las métricas de uso de CPU de un contenedor específico
query = 'container_cpu_usage_seconds_total{namespace="default"}'

# Ejecuta la consulta
results = prom.custom_query(query)

# El resultado será un diccionario con las métricas de uso de CPU
cpu_usage = float(results[0]['value'][1])
print("Uso de CPU (decimal):", cpu_usage)