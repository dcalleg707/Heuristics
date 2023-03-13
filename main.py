from read import *
from constructivo import constructivo
from store import storeData
import matplotlib.pyplot as plt

file = "test.txt"
nodesNumber, vehicles, capacity, autonomy, deposit, nodes = getData(file)

routes, distances, time = constructivo(nodes, vehicles, autonomy, capacity, True)
storeData(routes, distances, time)

fig, axs = plt.subplots(1, vehicles,  figsize=(9, 9), sharey=True)

index = 0
for route in routes:
    xAxis = [node[1] for node in nodes]
    yAxis = [node[2] for node in nodes]
    axs[index].scatter(xAxis, yAxis)

    xAxis = [nodes[node][1] for node in route]
    yAxis = [nodes[node][2] for node in route]
    axs[index].plot(xAxis, yAxis, label=str(index))
    index += 1

plt.show()



