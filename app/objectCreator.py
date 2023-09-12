#DEFINED ON enterNodes.html
def add_node(request, nodes_list):
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
        # 'location':     request.form['location'],
        'owner':        request.form['owner'],
        'comcap':       ((request.form['comcap']).split(', ')),
        'cores':        int(request.form['cores']),
        'percnormal':   float(request.form['percnormal']),
        'percsleeping': float(request.form['percsleeping'])
    }
    nodes_list.append(new_object)
    return nodes_list

#DEFINED ON enterTasks.html
def add_task(request, tasks_list):
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
    return tasks_list

#---------------------------------------TESTING---------------------------------------
if __name__ == "__main__":
    str = "HELLO WORLD"