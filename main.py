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

for i in range(1, 13):
    instance = "mtVRP" + str(i)
    file =  instance + ".txt"
    print(file)
    nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)
    cotaInferior = getCotaInferior(nodes)
    routes, distances, time = constructivoOptimizado(nodes, vehicles, autonomy, capacity)
    initialPheromone = Q/sum(distances)
    iterAntRoutes, iterAntDistances, iterAntTime = iterativeAntColony(nodes, vehicles, autonomy, capacity, m2, Q2, a2, b2, c, p2, initialPheromone, niter)
    antRoutes, antDistances, antTime = antColony(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, p, initialPheromone)
    noiseRoutes, noiseDistances, noiseTime = noise(nodes, vehicles, autonomy, capacity, r, stdDeviation, nsol)
    graspRoutes, graspDistances, graspTime = grasp(nodes, vehicles, autonomy, capacity, alpha, nsol)
    


    storeData(iterAntRoutes, iterAntDistances, iterAntTime, autonomy, "limited_ACO", instance)
    storeData(antRoutes, antDistances, antTime, autonomy, "ACO", instance)
    storeData(noiseRoutes, noiseDistances, noiseTime, autonomy, "NOISE", instance)
    storeData(graspRoutes, graspDistances, graspTime, autonomy, "GRASP", instance)
    storeData(routes, distances, time, autonomy, "Constructivo", instance)

    #barGraphic(["cota inferior", "constructivo", "NOISE", "GRASP", "ACO", "limited ACO"], [cotaInferior, sum(distances), sum(noiseDistances), sum(graspDistances), sum(antDistances), sum(iterAntDistances)], instance)
    #barGraphic(["constructivo", "NOISE", "GRASP", "ACO", "limited ACO"], [time, noiseTime, graspTime, antTime, iterAntTime], instance)

"""
file =  "mtVRP3.txt"
nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)
routes, distances, time = constructivoOptimizado(nodes, vehicles, autonomy, capacity)
initialPheromone = Q/sum(distances)
results = [[],[]]
times = [[],[]]
values = []

for i in range(10, 101, 10):
    value = i/100
    print(value)
    iterAntRoutes, iterAntDistances, iterAntTime = iterativeAntColony(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, value, initialPheromone, niter)
    antRoutes, antDistances, antTime = antColony(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, value, initialPheromone)
    results[0].append(sum(antDistances))
    results[1].append(sum(iterAntDistances))
    times[0].append(antTime)
    times[1].append(iterAntTime)
    values.append(value)

plotGraphic(values, results[0], f"ACO solution variations for different p values (m={m} Q={Q} a={a} b={b} c={c})")
plotGraphic(values, results[1], f"LACO solution variations for different p values (m={m} Q={Q} a={a} b={b} c={c} iterations={niter})")
plotGraphic(values, times[0], f"ACO time variations for different p values (m={m} Q={Q} a={a} b={b} c={c})")
plotGraphic(values, times[1], f"LACO time variations for different p values (m={m} Q={Q} a={a} b={b} c={c} iterations={niter})")
"""