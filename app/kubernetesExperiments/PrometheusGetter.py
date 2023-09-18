from prometheus_api_client import PrometheusConnect

prom = PrometheusConnect(url="http://localhost:30000")

def getMetricFromQuery(info, query):
    result = prom.custom_query(query)
    value = float(result[0]['value'][1])
    print(info,': ' ,value)
    return value

getMetricFromQuery('Uso de CPU (decimal)', 'container_cpu_usage_seconds_total{namespace="default"}')
getMetricFromQuery('Average power budget (watts)', 'machine_nvm_avg_power_budget_watts')