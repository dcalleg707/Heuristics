from read import *
from constructivo import constructivo
from store import storeData

file = "test.txt"
nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)

route, distances, time = constructivo(nodes, vehicles, autonomy, capacity)
storeData(route, distances, time)

