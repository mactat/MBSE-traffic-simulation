from sim import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import os

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


def createAnimation(X_list,Y_list,animation_speed = 10):
    anim_time = len(X_list[0])
    X_list = [lower_samples(X,animation_speed) for X in X_list]
    Y_list = [lower_samples(Y,animation_speed) for Y in Y_list]

    data_q = len(X_list)
    fig, ax = plt.subplots(data_q)
    plt.xlabel("meters")
    #plt.subplots_adjust(bottom=0.5,top=0.6)
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    colormap = np.array(['skyblue','b','y','g','r'])
    interval = int(1000/animation_speed)
    frames = int(anim_time/animation_speed)
    num_of_lanes = [len(np.unique(Y)) for Y in Y_list]

    def animate(i):
        for j in range(data_q):
            x = X_list[j][i]
            y = Y_list[j][i]
            ax[j].clear()
            ax[j].scatter(x, y, marker="s",c=colormap[np.array(y)],s=300)
            ax[j].set_xlim([0,10* 1000]) #10km
            ax[j].set_ylim([-1,num_of_lanes[j]])
            ax[j].set_title(f"sim {j}")
            ax[j].axhline(-0.5, linestyle='-', color='white')
            ax[j].axhline(0.5, linestyle='--', color='white')
            ax[j].axhline(1.5, linestyle='-', color='white')
            #ax[j].set_yticks([-0.5, 0.5, 1.5], minor=False)
            #ax[j].yaxis.grid(True, which='major')
            ax[j].axes.get_yaxis().set_visible(False)
            clearScreen()
            print(f"Animation time: {i/animation_speed:.2f}/{frames*interval/1000}s Real time: {i*animation_speed/60:.2f}/{anim_time/60:.2f}min")
    ani = FuncAnimation(fig, animate, frames=frames, interval=interval, repeat=False)
    plt.show()
    return


scheduler = Scheduler(
    num_of_lanes = 2, 
    highway_length = 10, 
    speed_limit = 90, #in km/h
    step_time = 1) # in sec

results = scheduler.sim_with_one_car(9)


X1,Y1 = dictToData(results)
X2,Y2 = dictToData(results)

createAnimation([X1,X2],[Y1,Y2], animation_speed= 10)