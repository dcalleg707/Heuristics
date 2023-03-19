from read import *
from constructivo import constructivo
from constructivoOptimizado import constructivoOptimizado
from constructivoOptimizadoExperimental import constructivoExperimental
from Grasp import grasp
from store import storeData
from graphics import *
from antColony import antColony

file = "mtVRP1.txt"
nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)
alpha = 0.02
nsol = 200
m = 2
Q = 2
a = 0.5
b = 1
p = 0.1


antRoutes, antDistances, antTime = antColony(nodes, vehicles, autonomy, capacity, m, Q, a, b, p)
print(antTime)
#graspRoutes, graspDistances, graspTime = grasp(nodes, vehicles, autonomy, capacity, alpha, nsol)
print("-----------------------------------")
routes, distances, time = constructivoOptimizado(nodes, vehicles, autonomy, capacity)
#storeData(routes, distances, time)
compare(routes, antRoutes, nodes, sum(distances), sum(antDistances), "constructivo", "ant")


