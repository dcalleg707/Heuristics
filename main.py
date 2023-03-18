from read import *
from constructivo import constructivo
from constructivoOptimizado import constructivoOptimizado
from Grasp import grasp
from store import storeData
from graphics import *

file = "mtVRP1.txt"
nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)

optimizedRoutes, optimizedDistances, optimizedTime = grasp(nodes, vehicles, autonomy, capacity, 0, seed=978)
print("-----------------------------------")
routes, distances, time = constructivoOptimizado(nodes, vehicles, autonomy, capacity)
#storeData(routes, distances, time)
compare(optimizedRoutes, routes, nodes, sum(optimizedDistances), sum(distances))


