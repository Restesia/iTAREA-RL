import json

original_data = [
    [10000000, 150000000, 0.3, 75, 2000, 1, 0.7, 150000000, [""], [""], "computing", "class0", "public", ["wlan"], 2, 30.0, 0.01],
    [10000000, 150000000, 0.3, 75, 2000, 1, 0.7, 150000000, [""], [""], "computing", "class1", "public", ["wlan"], 2, 30.0, 0.01],
    [10000000, 150000000, 0.3, 75, 2000, 1, 0.7, 150000000, [""], [""], "computing", "class2", "public", ["wlan"], 2, 30.0, 0.01]
]

# Crear una nueva lista de objetos JSON en el formato deseado
transformed_data = []
for item in original_data:
    transformed_item = {
        "name": "n" + str(original_data.index(item) + 1),
        "cpu": item[0],
        "bwup": item[1],
        "pwup": item[2],
        "maxenergy": item[3],
        "ram": item[4],
        "importance": item[5],
        "pwdown": item[6],
        "bwdown": item[7],
        "sensingunits": item[8],
        "peripherials": item[9],
        "typecore": item[10],
        "location": item[11],
        # "owner": item[12],
        # "comcap": item[13],
        "cores": item[14],
        "percnormal": item[15],
        # "percsleeping": item[16]
        
    }
    transformed_data.append(transformed_item)

# Convertir la lista de objetos JSON en una cadena JSON
json_data = json.dumps(transformed_data, indent=4)

# Imprimir el JSON resultante
print(json_data)
