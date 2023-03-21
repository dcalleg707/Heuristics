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

file = "mtVRP1.txt"
nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)
alpha = 0.05
nsol = 100
m = 5
Q = 100
a = 1
b = 5
c = 0.01
p = 0.9
niter = 50
r= 0
stdDeviation = 5


iterAntRoutes, iterAntDistances, iterAntTime = iterativeAntColony(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, p, niter)
antRoutes, antDistances, antTime = antColony(nodes, vehicles, autonomy, capacity, m, Q, a, b, c, p)
noiseRoutes, noiseDistances, noiseTime = noise(nodes, vehicles, autonomy, capacity, r, stdDeviation, nsol)
graspRoutes, graspDistances, graspTime = grasp(nodes, vehicles, autonomy, capacity, alpha, nsol)
routes, distances, time = constructivoOptimizado(nodes, vehicles, autonomy, capacity)


storeData(iterAntRoutes, iterAntDistances, iterAntTime, autonomy, "limited_ACO", file)
storeData(antRoutes, antDistances, antTime, autonomy, "ACO", file)
storeData(noiseRoutes, noiseDistances, noiseTime, autonomy, "NOISE", file)
storeData(graspRoutes, graspDistances, graspTime, autonomy, "GRASP", file)
storeData(routes, distances, time, autonomy, "Constructivo", file)

compare(iterAntRoutes, antRoutes, nodes, sum(iterAntDistances), sum(antDistances), "iter ants", "ants")


