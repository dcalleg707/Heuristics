from read import *
from constructivo import constructivo
from store import storeData
import matplotlib.pyplot as plt

file = "mtVRP1.txt"
nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)

routes, distances, time = constructivo(nodes, vehicles, autonomy, capacity, True)
storeData(routes, distances, time)

fig, axs = plt.subplots(1, 4,  figsize=(9, 9), sharey=True)

index = 0
for route in routes:
    xAxis = [nodes[node][1] for node in route]
    yAxis = [nodes[node][2] for node in route]
    print(xAxis)
    print(yAxis)
    axs[index].plot(xAxis, yAxis, label=str(index))
    index += 1

plt.show()



