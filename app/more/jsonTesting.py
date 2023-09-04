import json

#LIST
myList1 = [ {'nombre': 'Juan', 'edad': 25}, 'Julia', {'nombre': 'María', 'edad': 30}, 200, {'nombre': 'Carlos', 'edad': 22}]

#JSON
myJsonString = json.dumps(myList1)

#LIST AGAIN
myList2 = json.loads(myJsonString)

def convertListsToSetsFromMap(myList):
    for i in range(len(myList)):
        if isinstance(myList[i], list):
            myList[i] = set(myList[i])

#SET
convertListsToSetsFromMap(myList1)
mySet = myList1




#TEST
print("LIST:", myList1)
print("JSON:", myJsonString)
print("RES:", mySet)