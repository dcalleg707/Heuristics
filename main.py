from read import *
from constructivo import constructivo
from constructivoOptimizado import constructivoOptimizado
from constructivoOptimizadoExperimental import constructivoExperimental
from iterativeAntColony import iterativeAntColony
from Grasp import grasp
from store import storeData
from graphics import *
from antColony import antColony
from noise import noise
from cotaInferior import getCotaInferior
import random
import time
from math import e
import xlwt
import os
import xlrd
from xlutils.copy import copy as xl_copy

#Execution code at the end

def twoOpt(route, a, b):
  return route[:a+1] + route[a+1: b+1][::-1] + route[b+1:]

def crossTwoOpt (routeFrom, routeTo, a, b):
  return [routeFrom[:a+1] + routeTo[b+1:], routeTo[:b+1] + routeFrom[a+1:]   ]

def threeOpt(route, a, b, c):
  r1 = route[0:a+1] + route[a+1: b+1] + route[b+1 : c+1][::-1] + route[c+1:]
  r2 = route[0:a+1] + route[a+1: b+1][::-1] + route[b+1 : c+1] + route[c+1:]
  r3 = route[0:a+1] + route[a+1: b+1][::-1] + route[b+1 : c+1][::-1] + route[c+1:]
  r4 = route[0:a+1]  + route[b+1 : c+1] + route[a+1: b+1] + route[c+1:]
  r5 = route[0:a+1]  + route[b+1 : c+1] + route[a+1: b+1][::-1] + route[c+1:]
  r6 = route[0:a+1]  + route[b+1 : c+1][::-1] + route[a+1: b+1] + route[c+1:]
  r7 = route[0:a+1]  + route[b+1 : c+1][::-1] + route[a+1: b+1][::-1] + route[c+1:]
  return r1, r2, r3, r4, r5, r6, r7

def getBestThreeOpt(route, a, b, c):
  routes = threeOpt(route, a, b, c)
  bestRoute = None
  bestDistance = 0
  for i in range(len(routes)):
    newDistance = singleDistanceOrInvalid(routes[i])
    if newDistance:
      if bestRoute == None or newDistance < bestDistance:
        bestRoute = routes[i]
        bestDistance = newDistance
  return bestRoute

def swap(route, a, b):
  route = route.copy()
  temp = route[b]
  route[b] = route[a]
  route [a] = temp
  return route

def crossSwap(routeA, routeB, a, b):
  routeA = routeA.copy()
  routeB = routeB.copy()
  temp = routeB[b]
  routeB[b] = routeA[a]
  routeA[a] = temp
  return routeA, routeB

def insert(route, node, position):
  route = route.copy()
  offset = 1 if  node > position else 0
  removedNode = route.pop(node)
  route.insert( position + offset, removedNode)
  return route

def crossInsert(routeA, routeB, node, position):
  routeA2 = routeA.copy()
  routeB2 = routeB.copy()
  removedNode = routeA2.pop(node)
  routeB2.insert(position, removedNode)
  return routeA2, routeB2

def singleDistanceOrInvalid(route):
  currentCapacity = capacity
  distance = 0
  visited = []
  if(route[0] != 0 or route[-1] != 0):
    return None
  for i in range(len(route)):
    if route[i] in visited and route[i] != 0:
      return None
    visited.append(route[i])
    currentCapacity -= demands[route[i]]
    if(i <= len(route) - 2):
      distance += distanceMatrix[route[i]][route[i+1]]
    if route[i] == 0:
      currentCapacity = capacity
    if currentCapacity < 0:
      return None
  return round(distance, 2)


def distanceOrInvalid(routes):
  distance = 0
  for route in routes:
    routeDistance = singleDistanceOrInvalid(route)
    if routeDistance:
      distance += routeDistance
    else:
      return None
  return round(distance, 2)

def getFactivilityScore(route):
  distance = singleDistanceOrInvalid(route)
  if distance == None:
    return None
  return  max(distance - autonomy, 0)

def getNetFactivilityScore(route):
  distance = singleDistanceOrInvalid(route)
  if distance == None:
    return None
  return  distance - autonomy

def feasiblenessOrInvalid(routes):
  feasibleScore = 0
  for route in routes:
    routeFeasibleness = getFactivilityScore(route)
    if routeFeasibleness != None:
      feasibleScore += routeFeasibleness
    else:
      return None
  return round(feasibleScore, 2)

def feasiblenessNetOrInvalid(routes):
  feasibleScore = 0
  for route in routes:
    routeFeasibleness = getNetFactivilityScore(route)
    if routeFeasibleness != None:
      feasibleScore += routeFeasibleness
    else:
      return None
  return round(feasibleScore, 2)


def twoOptExecuter(routes, bestImprovement=True, T=None, distanceOrInvalid = distanceOrInvalid):
  bestSolution = routes
  bestDistance = distanceOrInvalid(routes)
  enhanced = None
  for route in range(len(routes)):
    for nodeFrom in range(1, len(routes[route])-3):
      for nodeTo in range(nodeFrom + 2, len(routes[route])-1):
        newSolution = routes.copy()
        newSolution[route] = twoOpt(newSolution[route], nodeFrom, nodeTo)
        newDistance = distanceOrInvalid(newSolution)
        if(newDistance != None and newDistance < bestDistance):
          if(not bestImprovement):
            return newSolution    
          enhanced = True
          bestSolution = newSolution
          bestDistance = newDistance
        elif T and newDistance != None and random.random() <= e**((bestDistance - newDistance) / T):
          if(not bestImprovement):
            return newSolution  
          enhanced = True
          bestSolution = newSolution
          bestDistance = newDistance
  return(enhanced and  bestSolution)

def crossTwoOptExecuter(routes, bestImprovement=True, T=None, distanceOrInvalid = distanceOrInvalid):
  bestSolution = routes
  bestDistance = distanceOrInvalid(routes)
  enhanced = None
  for i in range(len(routes)-1):
    for j in range(i+1, len(routes)):
      for nodeFrom in range(len(routes[i])-2):
        for nodeTo in range(len(routes[j])-2):
          newSolution = routes.copy()
          newRouteI, newRouteJ = crossTwoOpt(newSolution[i], newSolution[j], nodeFrom, nodeTo)
          newSolution[i] = newRouteI
          newSolution[j] = newRouteJ
          newDistance = distanceOrInvalid(newSolution)
          if(newDistance != None and newDistance < bestDistance):
            if(not bestImprovement):
              return newSolution    
            enhanced = True
            bestSolution = newSolution
            bestDistance = newDistance
          elif T and newDistance != None and random.random() <= e**((bestDistance - newDistance) / T):
            if(not bestImprovement):
              return newSolution  
            enhanced = True
            bestSolution = newSolution
            bestDistance = newDistance
  return(enhanced and  bestSolution)


def randomCrossTwoOptExecuter(routes, T=None, Aleatory=False, limit = 1000):
  GeneratedSolution = None
  bestDistance = distanceOrInvalid(routes)
  iter = 0
  while True:
    iter += 1
    i = random.randint(0, len(routes) - 1)
    j = random.randint(0, len(routes) - 1)
    if i == j or len(routes[i]) <= 2 or len(routes[j]) <= 2: 
      continue
    if iter > limit: 
      return routes
    nodeFrom = random.randint(0, len(routes[i])-2)
    nodeTo = random.randint(0, len(routes[j])-2)
    newSolution = routes.copy()
    newRouteI, newRouteJ = crossTwoOpt(routes[i], routes[j], nodeFrom, nodeTo)
    newSolution[i] = newRouteI
    newSolution[j] = newRouteJ
    newDistance = distanceOrInvalid(newSolution)
    if newDistance != None:
      return newSolution

def swapExecuter(routes, bestImprovement=True, T=None, distanceOrInvalid = distanceOrInvalid):
  bestSolution = routes
  bestDistance = distanceOrInvalid(routes)
  enhanced = None
  for route in range(len(routes)):
    for nodeFrom in range(1, len(routes[route])-1):
      for nodeTo in range(nodeFrom + 1, len(routes[route])-1):
        newSolution = routes.copy()
        newSolution[route] = swap(newSolution[route], nodeFrom, nodeTo)
        newDistance = distanceOrInvalid(newSolution)
        if(newDistance != None and newDistance < bestDistance):
          if(not bestImprovement):
            return newSolution    
          enhanced = True
          bestSolution = newSolution
          bestDistance = newDistance
        elif T and newDistance != None and random.random() <= e**((bestDistance - newDistance) / T):
          if(not bestImprovement):
            return newSolution  
          enhanced = True
          bestSolution = newSolution
          bestDistance = newDistance
  return(enhanced and  bestSolution)

def crossSwapExecuter(routes, bestImprovement=True, T=None, distanceOrInvalid = distanceOrInvalid):
  bestSolution = routes
  bestDistance = distanceOrInvalid(routes)
  enhanced = None
  for i in range(len(routes)-1):
    for j in range(i+1, len(routes)):
      for nodeFrom in range(1, len(routes[i])-1):
        for nodeTo in range(1, len(routes[j])-1):
          newSolution = routes.copy()
          newRouteI, newRouteJ = crossSwap(newSolution[i], newSolution[j], nodeFrom, nodeTo)
          newSolution[i] = newRouteI
          singleDistanceOrInvalid(newRouteI)
          newSolution[j] = newRouteJ
          newDistance = distanceOrInvalid(newSolution)
          if(newDistance != None and newDistance < bestDistance):
            if(not bestImprovement):
              return newSolution    
            enhanced = True
            bestSolution = newSolution
            bestDistance = newDistance
          elif T and newDistance != None and random.random() <= e**((bestDistance - newDistance) / T):
            if(not bestImprovement):
              return newSolution  
            enhanced = True
            bestSolution = newSolution
            bestDistance = newDistance 
  return(enhanced and  bestSolution)

def randomCrossSwapExecuter(routes, T=None):
  GeneratedSolution = None
  bestDistance = distanceOrInvalid(routes)
  while True:
    i = random.randint(1, len(routes) - 1)
    j = random.randint(1, len(routes) - 1)
    nodeFrom = random.randint(0, len(routes[i])-2)
    nodeTo = random.randint(0, len(routes[j])-2)
    newSolution = routes.copy()
    newRouteI, newRouteJ = crossSwap(newSolution[i], newSolution[j], nodeFrom, nodeTo)
    newSolution[i] = newRouteI
    newSolution[j] = newRouteJ
    newDistance = distanceOrInvalid(newSolution)
    if(newDistance != None and newDistance < bestDistance):
      return newSolution
    elif T and newDistance != None and random.random() <= e**((bestDistance - newDistance) / T):
      return newSolution

def insertExecuter(routes, bestImprovement=True, T=None, distanceOrInvalid = distanceOrInvalid):
  bestSolution = routes
  bestDistance = distanceOrInvalid(routes)
  enhanced = None
  for route in range(len(routes)):
    for nodeFrom in range(1, len(routes[route])-1):
      for nodeTo in range(1, len(routes[route])-1):
        if(nodeFrom != nodeTo):
          newSolution = routes.copy()
          newSolution[route] = insert(newSolution[route], nodeFrom, nodeTo)
          newDistance = distanceOrInvalid(newSolution)
          if(newDistance != None and newDistance < bestDistance):
            if(not bestImprovement):
              return newSolution    
            enhanced = True
            bestSolution = newSolution
            bestDistance = newDistance
          elif T and newDistance != None and random.random() <= e**((bestDistance - newDistance) / T):
            if(not bestImprovement):
              return newSolution  
            enhanced = True
            bestSolution = newSolution
            bestDistance = newDistance
  return(enhanced and bestSolution)

def crossInsertExecuter(routes, bestImprovement=True, T=None, distanceOrInvalid = distanceOrInvalid):
  bestSolution = routes
  bestDistance = distanceOrInvalid(routes)
  enhanced = None
  for i in range(len(routes)-1):
    for j in range(1, len(routes)):
      if(i != j):
        for nodeFrom in range(1, len(routes[i])-1):
          for nodeTo in range(1, len(routes[j])-1):
            newSolution = routes.copy()
            newRouteI, newRouteJ = crossInsert(newSolution[i], newSolution[j], nodeFrom, nodeTo)
            newSolution[i] = newRouteI
            newSolution[j] = newRouteJ
            newDistance = distanceOrInvalid(newSolution)
            if(newDistance != None and newDistance < bestDistance):
              if(not bestImprovement):
                return newSolution    
              enhanced = True
              bestSolution = newSolution
              bestDistance = newDistance
            elif T and newDistance != None and random.random() <= e**((bestDistance - newDistance) / T):
              if(not bestImprovement):
                return newSolution  
              enhanced = True
              bestSolution = newSolution
              bestDistance = newDistance 
  return(enhanced and  bestSolution)

def randomCrossInsertExecuter(routes, T=None, limit = 1000):
  GeneratedSolution = None
  bestDistance = distanceOrInvalid(routes)
  iter = 0
  while True:
    if(iter >= limit):
      return routes
    i = random.randint(1, len(routes) - 1)
    j = random.randint(1, len(routes) - 1)
    if i == j:
      ConnectionRefusedError
    nodeFrom = random.randint(0, len(routes[i])-2)
    nodeTo = random.randint(0, len(routes[j])-2)
    newSolution = routes.copy()
    newRouteI, newRouteJ = crossInsert(newSolution[i], newSolution[j], nodeFrom, nodeTo)
    newSolution[i] = newRouteI
    newSolution[j] = newRouteJ
    newDistance = distanceOrInvalid(newSolution)
    iter+= 1
    if(newDistance != None):
      return newSolution


def threeOptExecuter(routes, bestImprovement=True, T=None, distanceOrInvalid = distanceOrInvalid):
  bestSolution = routes
  bestDistance = distanceOrInvalid(routes)
  enhanced = None
  for route in range(len(routes)):
    for nodeFrom in range(1, len(routes[route])-5):
      for nodeMiddle in range(nodeFrom + 2, len(routes[route])-3):
        for nodeTo in range(nodeMiddle + 2, len(routes[route])-1):
          newSolution = routes.copy()
          newRoute = getBestThreeOpt(newSolution[route], nodeFrom, nodeMiddle, nodeTo)
          if newRoute != None:
            newSolution[route] = newRoute
            newDistance = distanceOrInvalid(newSolution)
            if(newDistance != None and newDistance < bestDistance):
              if(not bestImprovement):
                return newSolution    
              enhanced = True
              bestSolution = newSolution
              bestDistance = newDistance
            elif T and newDistance != None and random.random() <= e**((bestDistance - newDistance) / T):
              if(not bestImprovement):
                return newSolution  
              enhanced = True
              bestSolution = newSolution
              bestDistance = newDistance
  return(enhanced and  bestSolution) 

def subRouteSplitter(route):
  if(len(route) <= 1):
    return []
  subroutes = []
  currentSubroute = []
  for i in range(1, len(route)):
    if route[i] == 0:
      subroutes.append(currentSubroute)
      currentSubroute = []
    else:
      currentSubroute.append(route[i])
  return subroutes

def restoreRoute(subroutes):
  route = [0]
  for subroute in subroutes:
    route += subroute + [0]
  return route



def subrouteSwapper(subroutesA, subroutesB, a):
  subroutesA = subroutesA.copy()
  subroutesB = subroutesB.copy()
  subroutesB.append(subroutesA.pop(a))
  return subroutesA, subroutesB

def subrouteSwapperExecuter(routes, bestImprovement=True, T=None, distanceOrInvalid=None):
  bestSolution = routes
  bestDistance = feasiblenessOrInvalid(routes)
  enhanced = None
  for i in range(len(routes)-1):
    subRoutesA = subRouteSplitter(routes[i])
    for j in range(i, len(routes)):
      if(i != j):
        subRoutesB = subRouteSplitter(routes[j])
        for subrouteIndexA in range(1 , len(subRoutesA)):
          newSolution = routes.copy()
          newSubroutesI, newSubroutesJ = subrouteSwapper(subRoutesA, subRoutesB, subrouteIndexA)
          newSolution[i] = restoreRoute(newSubroutesI)
          newSolution[j] = restoreRoute(newSubroutesJ)
          newDistance = feasiblenessOrInvalid(newSolution)
          if(newDistance != None and newDistance < bestDistance):
            if(not bestImprovement):
              return newSolution    
            enhanced = True
            bestSolution = newSolution
            bestDistance = newDistance
          elif T and newDistance != None and random.random() <= e**((bestDistance - newDistance) / T):
            if(not bestImprovement):
              return newSolution  
            print("enhanced")
            enhanced = True
            bestSolution = newSolution
            bestDistance = newDistance 
  return(enhanced and  bestSolution)

def VNS(routes, algorithmExecuters, bestImprovement = True, T = None, niter = None, distanceOrInvalid=distanceOrInvalid, limitTime = None):
  bestSolution = routes
  start = time.time()
  algorithm = 0
  iter = 0
  while algorithm < len(algorithmExecuters):
    if niter and iter == niter:
      break
    newSolution = algorithmExecuters[algorithm](bestSolution, bestImprovement, T, distanceOrInvalid=distanceOrInvalid)
    if newSolution != None:
      bestSolution = newSolution
      algorithm = 0
    else:
      algorithm += 1
    iter+=1
    if(limitTime != None and time.time() - start > limitTime):
      return bestSolution
  return bestSolution

def VNSMSRSP(Ti, Tf, L, r, nsol, limitTime = None):
  index = 0
  absoluteBestSolution = None
  adbsoluteBestDistance = None
  start = time.time()
  for i in range(nsol):
    routes = grasp(nodes, vehicles, autonomy, capacity, 0.07, 1)[0]
    while(distanceOrInvalid(routes) == None):
      routes = grasp(nodes, vehicles, autonomy, capacity, 0.07, 10)[0]
    T = Ti
    index+=1
    iter = 0
    comparativeSolution = routes.copy()
    comparativeDistance = distanceOrInvalid(routes)
    bestSolution = routes.copy()
    bestDistance = distanceOrInvalid(routes)
    perturbedSolution = randomCrossTwoOptExecuter(comparativeSolution)
    while(distanceOrInvalid(perturbedSolution) == None):
      perturbedSolution = randomCrossTwoOptExecuter(comparativeSolution)
    comparativeSolution = perturbedSolution
    comparativeDistance = distanceOrInvalid(perturbedSolution)
    newSolution = comparativeSolution
    while T > Tf:
      if iter == L:
        iter = 0
        T = T*r
      iter += 1
      if(limitTime != None and time.time() - start > limitTime):
        return absoluteBestSolution if absoluteBestSolution != None else bestSolution 
      
      tempSolution = crossInsertExecuter(newSolution, T = T, bestImprovement=False)
      if tempSolution != None:
        newSolution = tempSolution
      tempSolution = insertExecuter(newSolution, T = T, bestImprovement=False)
      if tempSolution != None:
        newSolution = tempSolution
      newSolutionDistance = distanceOrInvalid(newSolution)
      if newSolutionDistance == None or newSolutionDistance == comparativeDistance:
        continue
      comparativeSolution = newSolution
      comparativeDistance =  newSolutionDistance
      if(newSolutionDistance < bestDistance):
          bestSolution = newSolution
          bestDistance = newSolutionDistance
      
    if (absoluteBestSolution == None) or (bestDistance < adbsoluteBestDistance):
      absoluteBestSolution = bestSolution
      adbsoluteBestDistance = bestDistance
  return absoluteBestSolution

def storeData(routes, distances, time, autonomy, name, instance):
    wb = None
    if(os.path.isfile("mtVRP_DavidCalleGonzalez_" + name + ".xls")):
        rb = xlrd.open_workbook("mtVRP_DavidCalleGonzalez_" + name + ".xls", formatting_info=True)
        wb = xl_copy(rb)
    else:
        wb = xlwt.Workbook("mtVRP_DavidCalleGonzalez_" + name + ".xls")
    sheet = wb.add_sheet(instance)
    feasable = 0
    for i in range(len(routes)):
        distanceA = singleDistanceOrInvalid(routes[i])
        sheet.write(i, len(routes[i]), distanceA)
        localFeasable = 0 if distanceA <= autonomy else 1
        feasable = feasable or localFeasable
        sheet.write(i, len(routes[i])+1, localFeasable)
        for j in range(len(routes[i])):
            sheet.write(i, j, routes[i][j])
    sheet.write(len(routes), 0, distanceOrInvalid(routes))
    sheet.write(len(routes), 1, round(time, 3))
    sheet.write(len(routes), 2, feasable)
    wb.save("mtVRP_DavidCalleGonzalez_" + name + ".xls")


alpha = 0.05
nsol = 30
m = 3
Q = 2
a = 4
b = 10
c = 1
p = 0.9

m2 = 6
Q2 = 1
a2 = 1
b2 = 17
p2= 0.3
niter = 8
r= 0
stdDeviation = 2

results = []
algorithms = [crossTwoOptExecuter, crossSwapExecuter, threeOptExecuter, insertExecuter, twoOptExecuter, swapExecuter, crossInsertExecuter, subrouteSwapperExecuter]
timeLimits =  [300,300,450,600,450,300,450,450,450,450,600,300]

for i in range(1, 13):
    results.append([])
    instance = "mtVRP" + str(i)
    file =  instance + ".txt"
    print(file)
    nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)
    distanceMatrix = getDistanceMatrix(nodes)
    demands = getDemands(nodes)
    routes, distances, constTime = constructivoOptimizado(nodes, vehicles, autonomy, capacity)
    initialPheromone = Q/sum(distances)
    iterAntRoutes, iterAntDistances, iterAntTime = iterativeAntColony(nodes, vehicles, autonomy, capacity, m2, Q2, a2, b2, c, p2, initialPheromone, niter)
    antRoutes, antDistances, antTime = antColony(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, p, initialPheromone)
    noiseRoutes, noiseDistances, noiseTime = noise(nodes, vehicles, autonomy, capacity, r, stdDeviation, nsol)
    graspRoutes, graspDistances, graspTime = grasp(nodes, vehicles, autonomy, capacity, alpha, nsol)

    VNS_start = time.time()
    VNS_solution = VNS(iterAntRoutes, algorithms, limitTime = timeLimits[i-1])
    VNS_time = time.time()

    VNSOpt_start = time.time()
    VNSOpt_solution = VNS(iterAntRoutes, algorithms, limitTime = timeLimits[i-1], distanceOrInvalid= feasiblenessOrInvalid)
    VNSOpt_time = time.time()

    VNSMSRSP_start = time.time()
    VNSMSRSP_solution =  VNSMSRSP(64, 0.01, 20, 0.7,3, limitTime = timeLimits[i-1])
    VNSMSRSP_time = time.time() - VNSMSRSP_start

    results[i-1].append(antRoutes)
    results[i-1].append(routes)
    results[i-1].append(graspRoutes)
    results[i-1].append(noiseRoutes)
    results[i-1].append(iterAntRoutes)
    results[i-1].append(VNS_solution)
    results[i-1].append(iterAntRoutes)
    

    storeData(VNS_solution, distanceOrInvalid(VNS_solution), abs(VNS_time), autonomy, "VNS", instance)
    storeData(VNSOpt_solution, distanceOrInvalid(VNSOpt_solution), abs(VNSOpt_time), autonomy, "VNSOpt", instance)
    storeData(VNSMSRSP_solution, distanceOrInvalid(VNSMSRSP_solution), abs(VNSMSRSP_time), autonomy, "VNSMSRSP", instance)
    #storeData(noiseVns, distanceOrInvalid(noiseVns) or noiseDistances, abs(endNoise), autonomy, "NOISE", instance)
    #storeData(graspVns, distanceOrInvalid(graspVns) or graspDistances, abs(endGrasp), autonomy, "GRASP", instance)
    #storeData(constructiveVns, distanceOrInvalid(constructiveVns) or distances, abs(endConst), autonomy, "Constructivo", instance)
    #barGraphic(["cota inferior", "constructivo", "NOISE", "GRASP", "ACO", "limited ACO"], [cotaInferior, sum(distances), sum(noiseDistances), sum(graspDistances), sum(antDistances), sum(iterAntDistances)], instance)
    #barGraphic(["constructivo", "NOISE", "GRASP", "ACO", "limited ACO"], [time, noiseTime, graspTime, antTime, iterAntTime], instance)