from flask import Flask, render_template, url_for, redirect, request
from imain import *
import subprocess
import json
import os
import datetime
from proccessor import proccess
from objectCreator import add_node, add_task
from isaver import saveAll

app=Flask(__name__)
nodes_list = []
tasks_list = []


#---------------------------------------ROUTES---------------------------------------

route = 'imain.py' #TRABAJO
#route = 'app_metrics/app/imain.py'
#route = 'app/imain.py' #PERSONAL

#---------------------------------------LOAD HTML TEMPLATES---------------------------------------

@app.route("/loadNodesTemplate")
def loadNodesTemplate():
    return render_template("enterNodes.html",  nodes_list=nodes_list, zip_lists=zip_lists)

@app.route("/loadTasksTemplate")
def loadTasksTemplate():
    return render_template("enterTasks.html", tasks_list=tasks_list, zip_lists=zip_lists)

@app.route("/readFile")
def readFile():
    return render_template("readFile.html")

@app.route("/printValues")
def printValues():
    nodes_json = json.dumps(nodes_list)
    tasks_json = json.dumps(tasks_list)
    output = loadData(nodes_json, tasks_json)
    return render_template('printValues.html', result=output, nodes=nodes_json, tasks=tasks_json, determine_back_route=determine_back_route)

#---------------------------------------ADD AND DELETE OBJECTS---------------------------------------

@app.route('/add_new_node', methods=['POST'])
def add_new_node():
    global nodes_list
    nodes_list = add_node(request, nodes_list)     #printAll(nodes_list)
    return redirect(url_for('loadNodesTemplate'))

@app.route('/add_new_task', methods=['POST'])
def add_new_task():
    global tasks_list
    tasks_list = add_task(request, tasks_list)     #printAll(tasks_list)
    return redirect(url_for('loadTasksTemplate'))

@app.route('/delete_node', methods=['POST'], )
def delete_node():
    delete_object(nodes_list)
    return redirect('/loadNodesTemplate')

@app.route('/delete_task', methods=['POST'])
def delete_task():
    delete_object(tasks_list)
    return redirect('/loadTasksTemplate')

#---------------------------------------FILE LOADING, WRITING AND UPDATING---------------------------------------

@app.route('/printHello', methods=['GET'])
def printHello():
    print("Hello")


@app.route('/processAndPrint', methods=['POST'])
def processAndPrint():
    if request.method == 'POST':
        nodes_json=""
        tasks_json=""
        output=""
        file = request.files['file_input']
        if file:
            try:
                nodes_json, tasks_json = proccess(file)
                output = loadData(nodes_json, tasks_json)
            except json.JSONDecodeError as json_error:
                error_message = f"Error decoding JSON: {json_error}"
                return render_template('printValues.html', result=error_message, nodes=nodes_json, tasks=tasks_json, determine_back_route=determine_back_route)
            except Exception as e:
                return render_template('printValues.html', result=str(e),nodes=nodes_json, tasks=tasks_json, determine_back_route=determine_back_route) 
        return render_template('printValues.html', result=output, nodes=nodes_json, tasks=tasks_json, determine_back_route=determine_back_route)

# @app.route("/printValues")
# def printValues():
#     output = loadData(json.dumps(nodes_list), json.dumps(tasks_list))
#     return render_template('printValues.html', result=output, determine_back_route=determine_back_route)

@app.route("/saveResult", methods=["POST"])
def saveResult():

    try:
        now = datetime.datetime.now()
        date_string = now.strftime("%d-%m-%y_%H.%M")
        filename = f"{date_string}.txt"
        location = request.form.get("location")

        if not location:    raise ValueError("La ubicación no puede estar vacía")
        filepath = os.path.join(location, filename)
        result = request.form.get("result", "")  # Obtener el contenido del resultado
        with open(filepath, "w") as file:   file.write(result)
        message = f"El resultado se ha guardado en {filepath}"

    except FileNotFoundError as e:
        message = f"Error al guardar el resultado: {str(e)}"
    except PermissionError as e:
        message = f"Error de permisos al guardar el resultado: {str(e)}"
    except ValueError as e:
        message = f"Error al guardar el resultado: {str(e)}"
    except Exception as e:
        message = f"Error inesperado al guardar el resultado: {str(e)}"

    return message

#---------------------------------------AUX FUNCTIONS---------------------------------------

def loadData(nodes_json, tasks_json):
    output=""
    try:
        output = subprocess.check_output(['python', route, nodes_json, tasks_json], text=True)
        if not output.strip(): 
            output = "No result"
    except subprocess.CalledProcessError as e:
        print("Error executing imain.py:", e)
        print("Error output:", e.output)
    return output

def zip_lists(a, b): return zip(a, b)

def printAll(list):
    for elem in list: print(elem)

def determine_back_route():
    current_path = request.referrer
    if current_path.endswith('loadTasksTemplate'):
        return 'loadTasksTemplate'  # Nombre de la función para entertasks.html
    elif current_path.endswith('readFile'):
        return 'readFile'  # Nombre de la función para readfile.html
    else:
        return 'index'  # Nombre de la función para la página de inicio
    
def delete_object(this_list):
    index = request.form['index']
    print(index)
    if index is not None and index.isdigit():
        index = int(index)
        print(index)
        if 0 <= index < len(this_list):
            del this_list[index]
    
#---------------------------------------MAIN FUNCTIONS---------------------------------------

@app.route('/')
def index():
    return render_template('index.html')
    #return render_template('index.html', data=data)

if __name__=='__main__':
    app.run(debug=True, port=5000) #removable options inside the function