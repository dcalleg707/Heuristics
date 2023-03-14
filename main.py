from read import *
from constructivo import constructivo
from constructivoOptimizado import constructivoOptimizado
from store import storeData
from graphics import *

file = "mtVRP12.txt"
nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)

optimizedRoutes, optimizedDistances, optimizedTime = constructivoOptimizado(nodes, vehicles, autonomy, capacity, False)
routes, distances, time = constructivo(nodes, vehicles, autonomy, capacity, False)
storeData(routes, distances, time)
compare(optimizedRoutes, routes, nodes, sum(optimizedDistances), sum(distances))


