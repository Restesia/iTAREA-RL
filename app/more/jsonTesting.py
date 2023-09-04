import json

#LIST <MAPS>
myList1 = [ {'nombre': 'Juan', 'edad': 25}, 'Julia', {'nombre': 'María', 'edad': 30}, 200, {'nombre': 'Carlos', 'edad': 22}]

#LIST -> JSON
myJsonString = json.dumps(myList1)

#JSON -> LIST
myList2 = json.loads(myJsonString)

def convertListsToSetsFromMap(myList):
    for i in range(len(myList)):
        if isinstance(myList[i], list):
            myList[i] = set(myList[i])

#LIST -> SET
convertListsToSetsFromMap(myList1)
mySet = myList1

#EMPTY SET
emptySet = set()

#SET
#fullSet =  set(myList1.get(emptySet, set())) 


#TEST
print("LIST:", myList1)
print("JSON:", myJsonString)
print("RES:", mySet)
print("EMPTY SET:", emptySet)