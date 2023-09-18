from prometheus_api_client import PrometheusConnect

# Conecta con el servidor Prometheus
prom = PrometheusConnect(url="http://localhost:30000")

# Define la consulta para obtener las métricas de uso de CPU de un contenedor específico
query1 = 'container_cpu_usage_seconds_total{namespace="default"}'
query2 = 'machine_nvm_avg_power_budget_watts'

# Ejecuta la consulta
results = prom.custom_query(query1)
results = prom.custom_query(query2)

# El resultado será un diccionario con las métricas de uso de CPU
cpu_usage = float(results[0]['value'][1])
print("Uso de CPU (decimal):", cpu_usage)