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

file = "mtVRP8.txt"

alpha = 0.05
nsol = 30
m = 3
Q = 1
a = 1
b = 5
c = 0.01
p = 0.9
p2 = 0.5
niter = 25
r= 0
stdDeviation = 5


for i in range(1, 13):
    instance = "mtVRP" + str(i)
    file =  instance + ".txt"
    print(file)
    nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)
    iterAntRoutes, iterAntDistances, iterAntTime = iterativeAntColony(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, p2, niter)
    antRoutes, antDistances, antTime = antColony(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, p)
    noiseRoutes, noiseDistances, noiseTime = noise(nodes, vehicles, autonomy, capacity, r, stdDeviation, nsol)
    graspRoutes, graspDistances, graspTime = grasp(nodes, vehicles, autonomy, capacity, alpha, nsol)
    routes, distances, time = constructivoOptimizado(nodes, vehicles, autonomy, capacity)


    storeData(iterAntRoutes, iterAntDistances, iterAntTime, autonomy, "limited_ACO", instance)
    storeData(antRoutes, antDistances, antTime, autonomy, "ACO", instance)
    storeData(noiseRoutes, noiseDistances, noiseTime, autonomy, "NOISE", instance)
    storeData(graspRoutes, graspDistances, graspTime, autonomy, "GRASP", instance)
    storeData(routes, distances, time, autonomy, "Constructivo", instance)


