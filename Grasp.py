from read import getDistanceMatrix, getDemands
import time
import random

def grasp(nodes, vehicles, autonomy, capacity, alpha, nsol, allowUnfeasibleness= True):
    global time
    start = time.time()
    bestRoutes = None
    bestDistances = None
    for i in range(nsol):
        routes, vehicleDistances = implementation(nodes, vehicles, autonomy, capacity, alpha, allowUnfeasibleness)
        if not bestDistances or sum(vehicleDistances) < sum(bestDistances):
            bestRoutes = routes
            bestDistances = vehicleDistances
    end = time.time()
    elapsedTime = end - start
    return bestRoutes, bestDistances, elapsedTime


def implementation(nodes, vehicles, autonomy, capacity, alpha, allowUnfeasibleness ):
    distanceMatrix = getDistanceMatrix(nodes)
    demands = getDemands(nodes)
    vehicleRoutes = []
    vehicleLoads = []
    vehicleDistances = []
    unvisitedNodes = nodes[1:]
    for i in range(vehicles):
        vehicleRoutes.append([nodes[0]])
        vehicleLoads.append(capacity)
        vehicleDistances.append(0)

    while(True):
        bestTruck, bestNode = getBestArch([route[-1] for route in vehicleRoutes], unvisitedNodes, distanceMatrix, vehicleLoads, vehicleDistances, autonomy, demands, alpha, allowUnfeasibleness)
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

def getBestArch(currentNodes, nodes, distanceMatrix, loads, traveledDistances, autonomy, demands,  alpha, allowUnfeasibleness ):
    minDistance = (-1, None)
    maxDistance = (-1, None)
    candidates = []
    limit = 0

    for i in range(len(currentNodes)):
        truckCandidates = getvalidNodesDistances(currentNodes[i], nodes, distanceMatrix, loads[i], traveledDistances[i], autonomy, demands, allowUnfeasibleness)
        candidates += list(map( lambda x: x + [i], truckCandidates))

    if not candidates:
        return None, None
    
    for candidate in candidates:
        if candidate[0] < minDistance[0] or minDistance[0] == -1:
            minDistance = candidate
        if candidate[0] > maxDistance[0]:
            maxDistance = candidate
    
    limit = minDistance[0] + alpha*(maxDistance[0] - minDistance[0])
    trueCandidates = [candidate for candidate in candidates if candidate[0] <= limit]
    chosenOne = trueCandidates[random.randint(0, len(trueCandidates) -1)]

    return chosenOne[2], chosenOne[1]

def getValidNearestNode(currentNode, nodes, distanceMatrix, load, traveledDistance, autonomy, demands,  allowUnfeasibleness):
    validNodes = getValidNodes(currentNode, nodes, distanceMatrix, load, traveledDistance, autonomy, demands,  allowUnfeasibleness)
    return getNearestNode(currentNode, validNodes, distanceMatrix)

def getvalidNodesDistances(currentNode, nodes, distanceMatrix, load, traveledDistance, autonomy, demands,  allowUnfeasibleness):
    validNodes = getValidNodes(currentNode, nodes, distanceMatrix, load, traveledDistance, autonomy, demands,  allowUnfeasibleness)
    return [[distanceMatrix[currentNode[0]][node[0]], node]for node in validNodes]

def getValidNodes(currentNode, nodes, distanceMatrix, load, traveledDistance, autonomy, demands,  allowUnfeasibleness):
    return  [node for node in nodes if (hasEnoughAutonomy(currentNode, node, distanceMatrix, traveledDistance, autonomy) or allowUnfeasibleness) and demands[node[0]] <= load and node != currentNode]

def hasToReturn(currentNode, nodes, distanceMatrix, load, traveledDistance, autonomy, demands,  allowUnfeasibleness):
    for node in nodes:
        if (hasEnoughAutonomy(currentNode, node, distanceMatrix, traveledDistance, autonomy) or allowUnfeasibleness) and demands[node[0]] <= load:
            return False
    return True

def getNearestNode(currentNode, nodes, distanceMatrix):
    nearestNode = currentNode
    minDistance = -1
    for node in nodes:
        if(distanceMatrix[currentNode[0]][node[0]] < minDistance or minDistance == -1):
            minDistance = distanceMatrix[currentNode[0]][node[0]]
            nearestNode = node
    return nearestNode, minDistance

def hasEnoughAutonomy(currentNode, destinyNode, distanceMatrix, traveledDistance, autonomy): 
    return  distanceMatrix[currentNode[0]][destinyNode[0]] + distanceMatrix[destinyNode[0]][0] + traveledDistance <= autonomy