import math

def getData(file):
    with open('test_cases/' + file, 'r') as f:
        lines = f.readlines()
        rows = [line.replace('\n', '').split("\t") for line in lines]
        initialData = rows[0]
        nodesNumber = initialData[0]
        vehicles = int(initialData[1])
        capacity = int(initialData[2])
        autonomy = int(initialData[3])
        deposit = rows[1]
        nodes = rows[1:]
        nodes = [list(map(lambda item: int(item),node)) for node in nodes]

    return nodesNumber, vehicles, capacity, autonomy, deposit, nodes

def getDistanceMatrix(nodes):
    matrix = []
    for nodeFrom in nodes:
        nodeFromIndex = int(nodeFrom[0])
        matrix.append([])
        for nodeTo in nodes:
            nodeToIndex = int(nodeTo[0])
            matrix[nodeFromIndex].append([])
            matrix[nodeFromIndex][nodeToIndex] = getDistance(nodeFrom[1], nodeFrom[2], nodeTo[1], nodeTo[2])
    return matrix

def getDemands(nodes):
    demands = []
    for node in nodes:
        demands.append(node[3])
    return demands
            

def getDistance(originx, originy, destinationx, destinationy):
    distancex = abs(originx - destinationx)
    distancey = abs(originy - destinationy)
    return round(math.sqrt(distancex**2 + distancey**2), 2)
