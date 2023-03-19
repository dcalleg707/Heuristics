from read import *
from constructivo import constructivo
from constructivoOptimizado import constructivoOptimizado
from constructivoOptimizadoExperimental import constructivoExperimental
from Grasp import grasp
from store import storeData
from graphics import *

file = "mtVRP8.txt"
nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)
alpha = 0.02
nsol = 200


optimizedRoutes, optimizedDistances, optimizedTime = constructivoOptimizado(nodes, vehicles, autonomy, capacity)
graspRoutes, graspDistances, graspTime = grasp(nodes, vehicles, autonomy, capacity, alpha, nsol)
print("-----------------------------------")
routes, distances, time = constructivoOptimizado(nodes, vehicles, autonomy, capacity)
#storeData(routes, distances, time)
compare(optimizedRoutes, graspRoutes, nodes, sum(optimizedDistances), sum(graspDistances), "constructivo", "grasp")


