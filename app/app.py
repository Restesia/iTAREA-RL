from flask import Flask, render_template, url_for, redirect, request
from imain import *
import subprocess
import json
import os
import datetime
import cgi
from proccessor import proccess

app=Flask(__name__)
nodes_list = []
tasks_list = []
stringsForm = cgi.FieldStorage()

#---------ROUTES---------
route = 'imain.py' #TRABAJO
#route = 'app_metrics/app/imain.py'
#route = 'app/imain.py' #PERSONAL


#---------LOAD HTML TEMPLATES---------
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
    output = loadData(json.dumps(nodes_list), json.dumps(tasks_list))
    return render_template('printValues.html', result=output, determine_back_route=determine_back_route)

#---------ADD AND DELETE---------

@app.route('/add_new_node', methods=['POST'])
def add_new_node():

    new_object = {
        'name':         request.form['name'],
        'cpu':          int(request.form['cpu']),
        'bwup':         int(request.form['bwup']),
        'pwup':         float(request.form['pwup']),
        'maxenergy':    int(request.form['maxenergy']),
        'ram':          int(request.form['ram']),
        'importance':   int(request.form['importance']),
        'pwdown':       float(request.form['pwdown']),
        'bwdown':       int(request.form['bwdown']),
        'sensingunits': (request.form['sensingunits'].split(', ')), #sensingunits = request.form['sensingunits']
        'peripherials': (request.form['peripherials'].split(', ')), #peripherials = request.form['peripherials']
        'typecore':     request.form['typecore'],
        'location':     request.form['location'],
        'owner':        request.form['owner'],
        'comcap':       ((request.form['comcap']).split(', ')),
        'cores':        int(request.form['cores']),
        'percnormal':   float(request.form['percnormal']),
        'percsleeping': float(request.form['percsleeping'])
    }
    nodes_list.append(new_object)
    #printAll(nodes_list)
    return redirect(url_for('loadNodesTemplate'))

@app.route('/add_new_task', methods=['POST'])
def add_new_task():
    new_object = {
        'taskname':     request.form['taskname'],
        'cpucycles':    int(request.form['cpucycles']),
        'ram':          int(request.form['ram']),
        'user':         int(request.form['user']),
        'mintransm':    int(request.form['mintransm']),
        'sensreq':      ((request.form['sensreq']).split(', ')), #set() es necesario, pero hace no serializable la app
        'periphreq':    ((request.form['periphreq']).split(', ')), 
        'transmit':     ((request.form['transmit']).split(', ')),
        'exlocation':   request.form['exlocation'],
        'tasktype':     request.form['tasktype'],
        'disk':         int(request.form['disk']),
    }
    tasks_list.append(new_object)
    #printAll(tasks_list)
    return redirect(url_for('loadTasksTemplate'))

@app.route('/delete_node', methods=['POST'], )
def delete_node():
    delete_object(nodes_list)
    return redirect('/loadNodesTemplate')

@app.route('/delete_task', methods=['POST'])
def delete_task():
    delete_object(tasks_list)
    return redirect('/loadTasksTemplate')

#---------LOAD MORE INFO---------

@app.route('/processAndPrint', methods=['POST'])
def processAndPrint():
    
    nodes_json=""
    tasks_json=""
    output=""

    if request.method == 'POST':
        file = request.files['file_input']
        if file:
            try:
                nodes_json, tasks_json = proccess(file)
                output = loadData(nodes_json, tasks_json)
            except json.JSONDecodeError as json_error:
                error_message = f"Error decoding JSON: {json_error}"
                return render_template('printValues.html', result=error_message, determine_back_route=determine_back_route)
            except Exception as e:
                return render_template('printValues.html', result=str(e), determine_back_route=determine_back_route) 
    return render_template('printValues.html', result=output, determine_back_route=determine_back_route)

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

#---------AUX FUNCTIONS---------

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

def zip_lists(a, b):     return zip(a, b)

def printAll(list):
    for elem in list:
        print(elem)

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
    
#---------MAIN FUNCTIONS---------

@app.route('/')
def index():
    return render_template('index.html')
    #return render_template('index.html', data=data)

if __name__=='__main__':
    app.run(debug=True, port=5000) #removable options inside the function