from read import getDistanceMatrix, getDemands
import time
import numpy

def noise(nodes, vehicles, autonomy, capacity, r, stdDeviation, nsol, allowUnfeasibleness= True):
    global time
    start = time.time()
    distanceMatrix = getDistanceMatrix(nodes)
    demands = getDemands(nodes)
    bestRoutes = None
    bestDistances = None
    for i in range(nsol):
        routes, vehicleDistances = implementation(nodes, vehicles, autonomy, capacity, distanceMatrix, demands, r, stdDeviation, allowUnfeasibleness)
        if not bestDistances or sum(vehicleDistances) < sum(bestDistances):
            bestRoutes = routes
            bestDistances = vehicleDistances
    end = time.time()
    elapsedTime = end - start
    return bestRoutes, bestDistances, elapsedTime

   


def implementation(nodes, vehicles, autonomy, capacity, distanceMatrix, demands,  r, stdDeviation, allowUnfeasibleness):
    
    vehicleRoutes = []
    vehicleLoads = []
    vehicleDistances = []
    unvisitedNodes = nodes[1:]
    for i in range(vehicles):
        vehicleRoutes.append([nodes[0]])
        vehicleLoads.append(capacity)
        vehicleDistances.append(0)

    while(True):
        bestTruck, bestNode = getBestArch([route[-1] for route in vehicleRoutes], unvisitedNodes, distanceMatrix, vehicleLoads, vehicleDistances, autonomy, demands, r, stdDeviation, allowUnfeasibleness)
        if not bestNode:
            break
        vehicleDistances[bestTruck] += distanceMatrix[vehicleRoutes[bestTruck][-1][0]][bestNode[0]]
        vehicleLoads[bestTruck] -= bestNode[3]
        vehicleRoutes[bestTruck].append(bestNode)
        unvisitedNodes.remove(bestNode)
        for i in range(vehicles):
            ret = hasToReturn(vehicleRoutes[i][-1], unvisitedNodes, distanceMatrix, vehicleLoads[i], vehicleDistances[i], autonomy, demands, allowUnfeasibleness)
            if(ret):
                vehicleDistances[i] += distanceMatrix[vehicleRoutes[i][-1][0]][0]
                vehicleLoads[i] = capacity
                vehicleRoutes[i].append(nodes[0])  
    routes = [list(map(lambda node:  node[0],nodes)) for nodes in vehicleRoutes]
    vehicleDistances = list (map(lambda x: round(x, 2),vehicleDistances))
    return routes, vehicleDistances

def getBestArch(currentNodes, nodes, distanceMatrix, loads, traveledDistances, autonomy, demands,  r, stdDeviation, allowUnfeasibleness):
    nextNode = None
    bestTruck = None
    minDistance = -1
    for i in range(len(currentNodes)):
        nearestNode, distance = getValidNearestNode(currentNodes[i], nodes, distanceMatrix, loads[i], traveledDistances[i], autonomy, demands, r, stdDeviation, allowUnfeasibleness)
        if(nearestNode == currentNodes[i]):
            continue
        elif(distance == minDistance and distance > 0):
            if(traveledDistances[i] < traveledDistances[bestTruck]):
                bestTruck = i
                minDistance = distance
                nextNode = nearestNode
        elif ((distance < minDistance and distance > 0) or minDistance == -1):
            bestTruck = i
            minDistance = distance
            nextNode = nearestNode
    return bestTruck, nextNode

def getValidNearestNode(currentNode, nodes, distanceMatrix, load, traveledDistance, autonomy, demands,  r, stdDeviation, allowUnfeasibleness):
    validNodes = [node for node in nodes if (hasEnoughAutonomy(currentNode, node, distanceMatrix, traveledDistance, autonomy) or allowUnfeasibleness) and demands[node[0]] <= load and node != currentNode]
    return getNearestNode(currentNode, validNodes, distanceMatrix ,r, stdDeviation)

def hasToReturn(currentNode, nodes, distanceMatrix, load, traveledDistance, autonomy, demands,  allowUnfeasibleness):
    if currentNode[0] == 0: return False
    for node in nodes:
        if (hasEnoughAutonomy(currentNode, node, distanceMatrix, traveledDistance, autonomy) or allowUnfeasibleness) and demands[node[0]] <= load:
            return False
    return True


def getNearestNode(currentNode, nodes, distanceMatrix, r, stdDeviation):
    nearestNode = currentNode
    minDistance = -1
    for node in nodes:
        if(distanceMatrix[currentNode[0]][node[0]] + numpy.random.normal(r, stdDeviation, 1)[0] < minDistance or minDistance == -1):
            minDistance = distanceMatrix[currentNode[0]][node[0]]
            nearestNode = node
    return nearestNode, minDistance

def hasEnoughAutonomy(currentNode, destinyNode, distanceMatrix, traveledDistance, autonomy): 
    return  distanceMatrix[currentNode[0]][destinyNode[0]] + distanceMatrix[destinyNode[0]][0] + traveledDistance <= autonomy