import matplotlib.pyplot as plt


def showTogether(routes, nodes):
    fig, ax = plt.subplots(1, 1,  figsize=(9, 9), sharey=True)

    index = 0
    xAxis = [node[1] for node in nodes]
    yAxis = [node[2] for node in nodes]
    ax.scatter(xAxis, yAxis)
    for route in routes:
        xAxis = [nodes[node][1] for node in route]
        yAxis = [nodes[node][2] for node in route]
        ax.plot(xAxis, yAxis, label=str(index))
        index += 1
    ax.legend()
    plt.show()

def showSeparated(routes, nodes):
    fig, axs = plt.subplots(1, len(routes),  figsize=(9, 9), sharey=True)
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

def compare(routesA, routesB, nodes, distanceA, distanceB, labelA, labelB):
    fig, axs = plt.subplots(1, 2,  figsize=(9, 9), sharey=True)

    
    index = 0
    xAxis = [node[1] for node in nodes]
    yAxis = [node[2] for node in nodes]
    axs[0].scatter(xAxis, yAxis)
    axs[1].scatter(xAxis, yAxis)
    index = 1
    for route in routesA:
        xAxis = [nodes[node][1] for node in route]
        yAxis = [nodes[node][2] for node in route]
        axs[0].plot(xAxis, yAxis, label=str(index))
        index += 1

    index = 1
    for route in routesB:
        xAxis = [nodes[node][1] for node in route]
        yAxis = [nodes[node][2] for node in route]
        axs[1].plot(xAxis, yAxis, label=str(index))
        index += 1

    axs[1].legend()
    axs[0].legend() 
    fig.suptitle(labelA +": " + str(round(distanceA, 2)) + " vs " + labelB +  ": "+str(round(distanceB, 2)))
    plt.show()

