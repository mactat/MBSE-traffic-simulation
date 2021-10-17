from traffic_simulation import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

scheduler = Scheduler(
    num_of_lanes =      5,
    average_speed =     8,
    average_speed_std = 10,
    speed_std =         3,
    car_freq =          4,
    sim_time =          1,
    sim_speed =         100
    )

flow1, results1 = scheduler.simulate(print_sim=True)\

scheduler = Scheduler(
    num_of_lanes =      5,
    average_speed =     8,
    average_speed_std = 0,
    speed_std =         0,
    car_freq =          4,
    sim_time =          1,
    sim_speed =         100
    )
    
flow2, results2 = scheduler.simulate(print_sim=False)
print(f"Results for simulation 1: {flow1}. Result for simulation 2: {flow2}")

#As result from simulation is in json format, it can be visualized anywhere(f.e on the website). For now i plot it in matplotlib.

def createAnimation(X_list,Y_list):
    data_q = len(X_list)
    fig, ax = plt.subplots(data_q)
    #plt.subplots_adjust(bottom=0.5,top=0.6)
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    colormap = np.array(['k','b','y','g','r'])

    def animate(i):
        for j in range(data_q):
            x = X_list[j][i]
            y = Y_list[j][i]
            ax[j].clear()
            ax[j].scatter(x, y, marker="s",c=colormap[np.array(y)])
            ax[j].set_xlim([0,150])
            ax[j].set_ylim([-1,5])
    ani = FuncAnimation(fig, animate, frames=len(X1), interval=50, repeat=False)
    plt.show()

X1,Y1 = jsonToData(results1)
X2,Y2 = jsonToData(results2)

createAnimation([X1,X2],[Y1,Y2])
