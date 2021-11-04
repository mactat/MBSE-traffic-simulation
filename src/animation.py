from sim import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import os
import json

#style
plt.rcParams.update({
"lines.color": "white",
"patch.edgecolor": "white",
"text.color": "black",
"axes.facecolor": "black",
"axes.edgecolor": "lightgray",
"axes.labelcolor": "white",
"xtick.color": "black",
"ytick.color": "white",
"grid.color": "lightgray",
"figure.facecolor": "white",
"figure.edgecolor": "white",
"savefig.facecolor": "white",
"savefig.edgecolor": "black"})


'''
Function for clening the screen, only needed in case of printing simulation in console
'''
def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def dictToData(results):
    
    # results.keys represents point in time ex. secods of animations
    # sample is a dict which contains informations about state of the lanes
    # key is a lane number , value is a dict which contains cars in form car.num:car.position

    X=[[car_pos for lane_num,cars in sample.items() for car_pos in cars.values()] for sample in results.values()]
    Y=[[int(lane_num)   for lane_num,cars in sample.items() for single_val in cars] for sample in results.values()]
    return X,Y

def lower_samples(sample_list, multiple):
    return [sample for i, sample in enumerate(sample_list) if i%multiple == 0]


def createAnimation(X_list,Y_list,animation_speed = 10, highway_length=10,num_of_lanes=2,reduce_data=10):
    anim_time = len(X_list[0])
    X_list = [lower_samples(X,reduce_data) for X in X_list]
    Y_list = [lower_samples(Y,reduce_data) for Y in Y_list]

    data_q = len(X_list)
    fig, ax = plt.subplots(data_q)
    plt.xlabel("meters")
    plt.subplots_adjust(bottom=0.3,top=0.7)
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    colormap = np.array(['skyblue','b','y','g','r'])
    interval = int(1000/animation_speed)
    frames = int(anim_time/reduce_data)

    def animate(i):
        for j in range(data_q):
            x = X_list[j][i]
            y = Y_list[j][i]
            ax[j].clear()
            for k in range(num_of_lanes[j]-1): ax[j].axhline(0.5 + k, linestyle='--', color='white')
            ax[j].scatter(x, y, marker="s",s=10)#c=colormap[np.array(y)])
            ax[j].set_xlim([0,highway_length* 1000]) #10km
            ax[j].set_ylim([-1,num_of_lanes[j]])
            # ax[j].set_title(f"sim {j}")
            ax[j].axhline(-0.5, linestyle='-', color='white')
            ax[j].axhline(num_of_lanes[j] - 0.5, linestyle='-', color='white')
            ax[j].axes.get_yaxis().set_visible(False)
            clearScreen()
            print(f"Animation time: {i/animation_speed:.2f}/{frames/animation_speed}s Real time: {i*animation_speed/60:.2f}/{anim_time/60:.2f}min")
    ani = FuncAnimation(fig, animate, frames=frames, interval=interval, repeat=False)
    plt.show()
    return


# ====================== examples =====================
highway_length = 2
num_of_lanes = 1

scheduler = Scheduler(
                        average_drivers_mood = 0.9 ,
                        num_of_lanes = num_of_lanes, 
                        highway_length = highway_length, 
                        speed_limit = 30, #in km/h
                        step_time = 1) # in sec

# two simulations with the same scheduler
sim_time = 10
inflow = 1
# results, results_dict = scheduler.sim_with_two_car(sim_time)
#scheduler.reset()
results, results_dict = scheduler.simulate(time_of_sim = sim_time, inflow = inflow) # cars per min->cannot be more than num of lanes

# results, results_dict = scheduler.sim_lane_changing(sim_time)

out_file = open("out.json", "w") 
json.dump(results_dict, out_file, indent = 6) 
out_file.close() 

X1,Y1 = dictToData(results_dict)
X2,Y2 = dictToData(results_dict)

createAnimation(
    [X1,X2], #x coord
    [Y1,Y2], #y coord
    animation_speed= 10,
    reduce_data = 10,
    highway_length=highway_length,
    num_of_lanes=[num_of_lanes,num_of_lanes]
    )

print(f"Results: {results}/{(sim_time-1)*inflow}")