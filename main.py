from Read import *
from constructivo import constructivo
import time


file = "test.txt"
nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)

start = time.time()
constructivo(nodes, vehicles, autonomy, capacity, True)
end = time.time()
print(end - start)

nodes = [[0,1,2]]
temp = []
