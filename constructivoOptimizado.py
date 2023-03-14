from read import getDistanceMatrix, getDemands
import time

def constructivoOptimizado(nodes, vehicles, autonomy, capacity, allowUnfeasibleness= True):
   global time
   start = time.time()
   routes, vehicleDistances = implementation(nodes, vehicles, autonomy, capacity, allowUnfeasibleness)
   end = time.time()
   elapsedTime = end - start
   return routes, vehicleDistances, elapsedTime


def implementation(nodes, vehicles, autonomy, capacity, allowUnfeasibleness):
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
        bestTruck, bestNode = getBestArch([route[-1] for route in vehicleRoutes], unvisitedNodes, distanceMatrix, vehicleLoads, vehicleDistances, autonomy, demands, allowUnfeasibleness)
        if not bestNode:
            break
        vehicleDistances[bestTruck] += distanceMatrix[vehicleRoutes[bestTruck][-1][0]][bestNode[0]]
        vehicleLoads[bestTruck] -= bestNode[3]
        vehicleRoutes[bestTruck].append(bestNode)
        unvisitedNodes.remove(bestNode)
        for i in range(vehicles):
            nextNode, distance = getValidNearestNode(vehicleRoutes[i][-1], unvisitedNodes, distanceMatrix, vehicleLoads[i], vehicleDistances[i], autonomy, demands, allowUnfeasibleness)
            if(nextNode == vehicleRoutes[i][-1] and nextNode != nodes[0]):
                vehicleDistances[i] += distanceMatrix[vehicleRoutes[i][-1][0]][0]
                vehicleLoads[i] = capacity
                vehicleRoutes[i].append(nodes[0])  
    routes = [list(map(lambda node:  node[0],nodes)) for nodes in vehicleRoutes]
    vehicleDistances = list (map(lambda x: round(x, 2),vehicleDistances))
    print(routes)
    print(vehicleDistances)
    print(unvisitedNodes)
    return routes, vehicleDistances

def getBestArch(currentNodes, nodes, distanceMatrix, loads, traveledDistances, autonomy, demands,  allowUnfeasibleness):
    nextNode = None
    bestTruck = None
    minDistance = -1
    for i in range(len(currentNodes)):
        nearestNode, distance = getValidNearestNode(currentNodes[i], nodes, distanceMatrix, loads[i], traveledDistances[i], autonomy, demands, allowUnfeasibleness)
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

def getValidNearestNode(currentNode, nodes, distanceMatrix, load, traveledDistance, autonomy, demands,  allowUnfeasibleness):
    validNodes = [node for node in nodes if (hasEnoughAutonomy(currentNode, node, distanceMatrix, traveledDistance, autonomy) or allowUnfeasibleness) and demands[node[0]] <= load and node != currentNode]
    return getNearestNode(currentNode, validNodes, distanceMatrix)

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