from sim import *
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import seaborn as sns

def test(params, features):
    scheduler = Scheduler(
        average_drivers_mood =    params['average_drivers_mood'],
        num_of_lanes =            params['Number of lanes'],
        highway_length =          params['Highway length [km]'],
        speed_limit =             params['Speed limit [km/h]'],
        step_time =               1,
        propotion_of_autonomous = params['Propotion of Autonomous cars [%]']/100,
        propotion_of_trucks = params['Propotion of Trucks [%]']/100)

    params['Flow'], _, params['Average speed [km/h]'] = scheduler.simulate(params['Simulation time [s]'],params['Inflow [vehicle/minute]'])
    return [params[single_feature] for single_feature in features]

params_dict={
    'Inflow [vehicle/minute]':          35,
    'Simulation time [s]':              10,
    'average_drivers_mood':             0.85,
    'Number of lanes':                  3,
    'Highway length [km]':              4,
    'Speed limit [km/h]':               110,
    'Propotion of Autonomous cars [%]': 0,
    'Propotion of Trucks [%]':          0,
    'Flow':                             0, #result
    'Average speed [km/h]':             0  #result
}

sim_results = []

# ====================== params =================

features = ['Propotion of Autonomous cars [%]', 'Propotion of Trucks [%]', 'Flow']
ranges = [np.arange(0,50,10),np.arange(0,50,10)]
style = "plot3d" # heatmap, plot3d

# ===============================================


k = 0
for i in ranges[0]:
    for j in ranges[1]:
        params_dict[features[0]] = i
        params_dict[features[1]] = j
        single_result = test(params_dict, features)
        sim_results.append(single_result)
        print(f"Solved {k} simulations.")
        k += 1 

sim_results = np.asarray(sim_results).T
x, y, z = sim_results[0], sim_results[1], sim_results[2]
if style == "plot3d":
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_xlabel(features[0])
    ax.set_ylabel(features[1])
    ax.set_zlabel(features[2])
    surf = ax.plot_trisurf(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
    fig.colorbar(surf, shrink=0.5, aspect=5)

if style == "heatmap":
    c = np.reshape(z,(len(ranges[0]),len(ranges[1])))
    ax = sns.heatmap(c, xticklabels=ranges[1], yticklabels=ranges[0])
    ax.set(title = features[2])
    ax.invert_yaxis()
    plt.xlabel(features[1], fontsize = 10)
    plt.ylabel(features[0], fontsize = 10)



plt.show()
