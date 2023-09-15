import json

#MAIN METHOD: RECEIVES DATA STORAGE, RETURNS TWO JSON STRINGS (NODES AND TASKS)
def proccess(file):
    file_content, file_extension = getContentAndExtension(file)                 #BIEN
    nodes_list, tasks_list = classifyAndGetData(file_content, file_extension)   #MAL
    return nodes_list, tasks_list

#---------------------------------------AUX METHODS---------------------------------------

def getContentAndExtension(file):
    file_content = ((file.read()).decode('utf-8'))
    #file_content = ''.join(file_content.splitlines())   #STRING
    file_extension = (file.filename).rsplit('.', 1)[-1].lower()     #STRING
    return file_content, file_extension

def classifyAndGetData(file_content, file_extension):
    if(file_extension=="json"):
        return json_read(file_content)    
    if(file_extension=="txt"):
        return txt_read(file_content)
    if(file_extension=="py"):
        return python_read(file_content)
    else: return "",""

#---------------------------------------READERS---------------------------------------

def json_read(file_content):
    nodes = []
    tasks = []
    try:
        data = json.loads(file_content)
        for item in data:
            if 'name' in item:
                nodes.append(item)
            elif 'taskname' in item:
                tasks.append(item)
        nodes_json_string = json.dumps(nodes)
        tasks_json_string = json.dumps(tasks)
        return nodes_json_string, tasks_json_string
    except json.JSONDecodeError as e:
        print("Error al decodificar el JSON:", str(e))
        return None, None

def txt_read(file_content):
    return json_read(file_content)

def python_read(file_content):
    return json_read(file_content)

#---------------------------------------TESTING---------------------------------------
if __name__ == "__main__":
    str = "HELLO WORLD"
    fe = "py"
    classifyAndGetData(str, fe)