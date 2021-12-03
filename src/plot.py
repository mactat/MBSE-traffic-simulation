import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import seaborn as sns

sim_results = np.genfromtxt('test3.csv', delimiter=',').T

features = ['Propotion of Autonomous cars [%]', 'Speed Limit [km/h]', 'Flow', 'Average Speed [km/h]']
ranges = [np.arange(0,101,10),np.arange(50,131,10)]
style = "plot3d" # heatmap, plot3d

x, y, z, avg_speed = sim_results[0]*100, sim_results[1], sim_results[2], sim_results[3]
if style == "plot3d":
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_xlabel(features[0])
    ax.set_ylabel(features[1])
    ax.set_zlabel(features[2])
    surf = ax.plot_trisurf(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
    fig.colorbar(surf, shrink=0.5, aspect=5)

if style == "heatmap":
    c = np.reshape(avg_speed,(len(ranges[0]),len(ranges[1])))
    ax = sns.heatmap(c, xticklabels=ranges[1], yticklabels=ranges[0])
    ax.set(title = features[3])
    ax.invert_yaxis()
    plt.xlabel(features[1], fontsize = 10)
    plt.ylabel(features[0], fontsize = 10)

plt.show()
