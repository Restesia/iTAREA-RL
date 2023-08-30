import json

#MAIN METHOD: RECEIVES DATA STORAGE, RETURNS TWO JSON STRINGS
def proccess(file):
    file_content, file_extension = getContentAndExtension(file)
    nodes_list, tasks_list = classifyAndGetData(file_content, file_extension)
    return nodes_list, tasks_list

def classifyAndGetData(file_content, file_extension):
    # Identificar el tipo
    if(file_extension=="json"): return json_read(file_content)    
    if(file_extension=="txt"):  return txt_read(file_content)
    if(file_extension=="py"):   return python_read(file_content)
    else: return "",""

#---------------------------------------------------

def json_read(file_content):
    nodes_json = []
    tasks_json = []

    lines = file_content.strip().split('\n')

    for line_number, line in enumerate(lines, start=1):
        data = json.loads(line)
        if "name" in data and "cpu" in data:
            nodes_json.append(data)
        elif "taskname" in data and "cpucycles" in data:
            tasks_json.append(data)

    nodes_json_string = "[" + ", ".join([json.dumps(item) for item in nodes_json]) + "]"
    tasks_json_string = "[" + ", ".join([json.dumps(item) for item in tasks_json]) + "]"

    return nodes_json_string, tasks_json_string


def txt_read(file_content):
    return json_read(file_content)

def python_read(file_content):
    return json_read(file_content)

def getContentAndExtension(file):
    file_content = (file.read()).decode('utf-8')                #STRING
    file_extension = (file.filename).rsplit('.', 1)[-1].lower() #STRING
    return file_content, file_extension

#PRUEBAS
if __name__ == "__main__":
    str = "HOLA"
    fe = "py"
    classifyAndGetData(str, fe)