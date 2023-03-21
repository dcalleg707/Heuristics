from read import getDistanceMatrix, getDemands
import time
import random

def iterativeAntColony(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, p, iteraciones, allowUnfeasibleness=True):
    global time
    start = time.time()
    routes, vehicleDistances = implementation(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, p, iteraciones, allowUnfeasibleness)
    end = time.time()
    elapsedTime = end - start
    return routes, vehicleDistances, elapsedTime


def implementation(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, p, iteraciones, allowUnfeasibleness ):
    distanceMatrix = getDistanceMatrix(nodes)
    demands = getDemands(nodes)
    
    pheromoneMatrix = []
    for i in range(len(nodes)):
        pheromoneMatrix.append([])
        for j in range (len(nodes)):
            pheromoneMatrix[i].append(1)
    
    minDistance = -1
    bestRoute = None
    bestDistances = None
    for z in range(iteraciones):
        antTrips = []
        solutionDistances = []
        for l in range(m):
            routes, distances = getAntRoute(nodes, autonomy, vehicles, distanceMatrix, capacity, demands, pheromoneMatrix, a, b, c, allowUnfeasibleness)
            distance = sum(distances)
            solutionDistances.append(distance)
            if(distance < minDistance or minDistance == -1):
                bestRoute = routes
                minDistance = distance
                bestDistances = distances
            antTrips.append(routes)

        newPheromoneMatrix = list(map(lambda pheromoneRow: list(map( lambda x: x * (1 - p), pheromoneRow)), pheromoneMatrix ))
        for i in range(len(antTrips)):
            for route in antTrips[i]:
                for j in range(len(route)-1):
                    newPheromoneMatrix[route[j]][route[j+1]] += Q / solutionDistances[i]

        pheromoneMatrix = newPheromoneMatrix

    return bestRoute, bestDistances

def getAntRoute(nodes, autonomy, vehicles, distanceMatrix, capacity, demands, pheromoneMatrix, a, b, c, allowUnfeasibleness):
    vehicleRoutes = []
    vehicleLoads = []
    vehicleDistances = []
    unvisitedNodes = nodes[1:]
    for i in range(vehicles):
        vehicleRoutes.append([nodes[0]])
        vehicleLoads.append(capacity)
        vehicleDistances.append(0)

    while(True):
        bestTruck, bestNode = getBestArch([route[-1] for route in vehicleRoutes], unvisitedNodes, distanceMatrix, vehicleLoads, vehicleDistances, autonomy, demands, pheromoneMatrix, a, b, c, allowUnfeasibleness)
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



def getBestArch(currentNodes, nodes, distanceMatrix, loads, traveledDistances, autonomy, demands, pheromoneMatrix, a, b, c, allowUnfeasibleness ):
    candidates = []
    probabilities = []
    sumedDivisor = 0

    for i in range(len(currentNodes)):
        truckCandidates = getvalidNodesDistances(currentNodes[i], nodes, distanceMatrix, loads[i], traveledDistances[i], autonomy, demands, allowUnfeasibleness)
        candidates += list(map( lambda x: x + [i], truckCandidates))
        localProbability =  list(map( lambda x: (( 1 / max(x[0], 0.0000001)) ** b) * (pheromoneMatrix[currentNodes[i][0]][x[1][0]] ** a) * ((1 / max(traveledDistances[i], 1)) ** c), truckCandidates))
        probabilities += localProbability
        sumedDivisor += sum(localProbability)
    

    if not candidates:
        return None, None
    if sumedDivisor == 0:
        sumedDivisor = len(probabilities)
        probabilities = map(lambda x: 1, probabilities)
    probabilities = list(map(lambda x: x / sumedDivisor, probabilities))
    chosenOne = random.choices(candidates, weights=probabilities, k=1)[0]

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