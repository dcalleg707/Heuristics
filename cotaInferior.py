from read import getDistanceMatrix

def getCotaInferior(nodes):
    miniumDistance = 0
    nodesNumber = len(nodes)
    distanceMatrix = getDistanceMatrix(nodes)
    for i in range(nodesNumber):
        miniumDistance += min(distanceMatrix[i][:i] +distanceMatrix[i][i+1:])
    distanceMatrix[0].remove(min(distanceMatrix[0][1:]))
    miniumDistance += min(distanceMatrix[0])
    return miniumDistance