from flask import Flask, render_template, url_for, redirect, request, jsonify
from imain import *
import subprocess
import json
import os

app=Flask(__name__)
nodes_list = []
tasks_list = []
route = 'imain.py' #app_metrics/app/imain.py

@app.route("/getNodesFromParameters")
def getNodesFromParameters():
    return render_template("enterNodes.html",  nodes_list=nodes_list, zip_lists=zip_lists)

@app.route("/getTasksFromParameters")
def getTasksFromParameters():
    return render_template("enterTasks.html", tasks_list=tasks_list, zip_lists=zip_lists)

@app.route("/readFile")
def readFile():
    # Aquí puedes realizar cualquier lógica adicional que necesites
    return render_template("readFile.html")

@app.route("/printValues")
def printValues():

    nodes_json = json.dumps(nodes_list)
    tasks_json = json.dumps(tasks_list)
    output=""

    try:
        output = subprocess.check_output(['python', route, nodes_json, tasks_json], text=True)
        if not output.strip():  # Verificar si el resultado está vacío
            output = "No result"
    except subprocess.CalledProcessError as e:
        print("Error executing imain.py:", e)
        print("Error output:", e.output)
    
    return render_template('printValues.html', result=output)

@app.route('/add_new_node', methods=['POST'])
def add_new_node():

    name = request.form['name']
    cpu = request.form['cpu']
    bwup = request.form['bwup']
    pwup = request.form['pwup']
    maxenergy = request.form['maxenergy']
    ram = request.form['ram']
    importance = request.form['importance']
    pwdown = request.form['pwdown']
    bwdown = request.form['bwdown']
    sensingunits = request.form['sensingunits']
    peripherials = request.form['peripherials']
    typecore = request.form['typecore']
    location = request.form['location']
    owner = request.form['owner']
    comcap = request.form['comcap']
    cores = request.form['cores']
    percnormal = request.form['percnormal']
    percsleeping = request.form['percsleeping']

    new_object = {
        'name':name,
        'cpu': cpu,
        'bwup': bwup,
        'pwup': pwup,
        'maxenergy':maxenergy,
        'ram':ram,
        'importance':importance,
        'pwdown':pwdown,
        'bwdown':bwdown,
        'sensingunits':sensingunits,
        'peripherials':peripherials,
        'typecore':typecore,
        'location':location,
        'owner':owner,
        'comcap':comcap,
        'cores':cores,
        'percnormal':percnormal,
        'percsleeping':percsleeping
    }

    nodes_list.append(new_object)
    #printAll(nodes_list)
    return redirect(url_for('getNodesFromParameters'))

@app.route('/add_new_task', methods=['POST'])
def add_new_task():

    taskname = request.form['taskname']
    cpucycles = request.form['cpucycles']
    ram = request.form['ram']
    user = request.form['user']
    mintransm = request.form['mintransm']
    sensreq = request.form['sensreq']
    periphreq = request.form['periphreq']
    transmit = request.form['transmit']
    exlocation = request.form['exlocation']
    tasktype = request.form['tasktype']
    disk = request.form['disk']


    new_object = {
        'taskname': taskname,
        'cpucycles': cpucycles,
        'ram':ram,
        'user':user,
        'mintransm':mintransm,
        'sensreq':sensreq,
        'periphreq':periphreq,
        'transmit':transmit,
        'exlocation':exlocation,
        'tasktype':tasktype,
        'disk':disk,
    }

    tasks_list.append(new_object)
    #printAll(tasks_list)
    return redirect(url_for('getTasksFromParameters'))

def printAll(list):
    for elem in list:
        print(elem)

    
def zip_lists(a, b):
    return zip(a, b)

@app.route('/delete_node', methods=['POST'], )
def delete_node():
    
    index = request.form['index']
    print(index)
    if index is not None and index.isdigit():
        index = int(index)
        print(index)
        if 0 <= index < len(nodes_list):
            del nodes_list[index]
    return redirect('/getNodesFromParameters')

@app.route('/delete_task', methods=['POST'])
def delete_task():
    index = request.form['index']
    print(index)
    if index is not None and index.isdigit():
        index = int(index)
        print(index)
        if 0 <= index < len(tasks_list):
            del tasks_list[index]
    return redirect('/getTasksFromParameters')

@app.route("/saveResult", methods=["POST"])
def saveResult():
    filename = request.form["filename"]
    location = request.form["location"]
    filepath = os.path.join(location, filename + ".txt")

    try:
        with open(filepath, "w") as file:
            file.write(request.args.get("result", ""))
        message = f"El resultado se ha guardado en {filepath}"
    except Exception as e:
        message = f"Error al guardar el resultado: {str(e)}"

    return render_template('saveResult.html', message=message)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file_input']
        if file:

            # Procesamiento del archivo cargado (leer el contenido del archivo y hacer algo con él). ¿Pandas?
            # Puedes utilizar bibliotecas como pandas para procesar archivos CSV.
            file_content = file.read()
            
            # Procesar el contenido del archivo como desees (puedes imprimirlo para verlo en la consola)
            print("CONTENT:"+"\n")
            print(file_content)

            # Guardar el contenido del archivo en una lista, diccionario u otra estructura de datos

    return redirect(url_for('index'))  # Redirige de nuevo a la página principal después de procesar el archivo

   

@app.route('/')
def index():

    #example_list = ['element1','element2','element3']
    #data={
    #    'title':'Metrics to energy app',
    #    'hi':"Hello!",
    #    'example_list':example_list,
    #    'list_length':len(example_list)
    #}

    return render_template('index.html'
                           #, data=data
                           )

if __name__=='__main__':
    app.run(debug=True, port=5000) #removable options inside the function