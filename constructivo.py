from read import getDistanceMatrix, getDemands
import time

def constructivo(nodes, vehicles, autonomy, capacity, allowUnfeasibleness= False):
   global time
   start = time.time()
   routes, vehicleDistances = implementation(nodes, vehicles, autonomy, capacity, allowUnfeasibleness)
   end = time.time()
   time = end - start
   return routes, vehicleDistances, time


def implementation(nodes, vehicles, autonomy, capacity, allowUnfeasibleness):
    distanceMatrix = getDistanceMatrix(nodes)
    demands = getDemands(nodes)
    vehicleRoutes = []
    vehicleLoads = []
    vehicleDistances = []
    completedVehicles = 0
    unvisitedNodes = nodes[1:]
    for i in range(vehicles):
        vehicleRoutes.append([nodes[0]])
        vehicleLoads.append(capacity)
        vehicleDistances.append(0)

    while( completedVehicles < vehicles):
        completedVehicles = 0
        for i in range(vehicles):
            nextNode = getValidNearestNode(vehicleRoutes[i][-1], unvisitedNodes, distanceMatrix, vehicleLoads[i], vehicleDistances[i], autonomy, demands, allowUnfeasibleness)
            if nextNode != vehicleRoutes[i][-1]:
                vehicleDistances[i] += distanceMatrix[vehicleRoutes[i][-1][0]][nextNode[0]]
                vehicleLoads[i] -= nextNode[3]
                vehicleRoutes[i].append(nextNode)
                unvisitedNodes.remove(nextNode)
            elif vehicleRoutes[i][-1] == nodes[0]:
                completedVehicles += 1
            else:
                vehicleDistances[i] += distanceMatrix[vehicleRoutes[i][-1][0]][0]
                vehicleLoads[i] = capacity
                vehicleRoutes[i].append(nodes[0])  
    routes = [list(map(lambda node:  node[0],nodes)) for nodes in vehicleRoutes]
    vehicleDistances = list (map(lambda x: round(x, 2),vehicleDistances))
    print(routes)
    print(vehicleDistances)
    print(unvisitedNodes)
    return routes, vehicleDistances
    

    

def getValidNearestNode(currentNode, nodes, distanceMatrix, load, traveledDistance, autonomy, demands,  allowUnfeasibleness = False):
    validNodes = [node for node in nodes if (hasEnoughAutonomy(currentNode, node, distanceMatrix, traveledDistance, autonomy) or allowUnfeasibleness) and demands[node[0]] <= load and node != currentNode]
    return getNearestNode(currentNode, validNodes, distanceMatrix)

def getNearestNode(currentNode, nodes, distanceMatrix):
    nearestNode = currentNode
    minDistance = -1
    for node in nodes:
        if(distanceMatrix[currentNode[0]][node[0]] < minDistance or minDistance == -1):
            minDistance = distanceMatrix[currentNode[0]][node[0]]
            nearestNode = node
    return nearestNode

def hasEnoughAutonomy(currentNode, destinyNode, distanceMatrix, traveledDistance, autonomy): 
    return  distanceMatrix[currentNode[0]][destinyNode[0]] + distanceMatrix[destinyNode[0]][0] + traveledDistance <= autonomy 

    







