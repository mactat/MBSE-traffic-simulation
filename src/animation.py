from sim import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import numpy as np
import os
import json
import random

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
    colors = [[car_num for lane_num,cars in sample.items() for car_num in cars.keys()] for sample in results.values()]
    print("X=",results.values())
    return X,Y,colors

def lower_samples(sample_list, multiple):
    return [sample for i, sample in enumerate(sample_list) if i%multiple == 0]


def createAnimation(results_list,animation_speed = 10, highway_length=10,num_of_lanes=2,reduce_data=10,export_gif_path=None):
    all_results = [dictToData(results) for results in results_list]
    X_list = [resultls[0] for resultls in all_results]
    Y_list = [resultls[1] for resultls in all_results]
    colors_list = [resultls[2] for resultls in all_results]

    anim_time = len(X_list[0])
    X_list = [lower_samples(X,reduce_data) for X in X_list]
    Y_list = [lower_samples(Y,reduce_data) for Y in Y_list]
    colors_list = [lower_samples(colors,reduce_data) for colors in colors_list]

    data_q = len(X_list)
    fig, ax = plt.subplots(data_q,sharex=True, squeeze=False)
    plt.xlabel("meters")
    size_adj = num_of_lanes[0]/100
    plt.subplots_adjust(bottom=(0.4-size_adj),top=(0.6+size_adj))
    plt.set_cmap('gist_rainbow')
    manager = plt.get_current_fig_manager()
    #manager.full_screen_toggle()
    colormap = np.array(['skyblue','b','y','g','r'])
    interval = int(1000/animation_speed)
    frames = int(anim_time/reduce_data)

    def animate(i):
        for j in range(data_q):
            x = X_list[j][i]
            y = Y_list[j][i]
            c = colors_list[j][i]
            ax[j][0].clear()
            for k in range(num_of_lanes[j]-1): ax[j][0].axhline(0.5 + k, linestyle='--', color='white')
            ax[j][0].scatter(x, y, marker="s",s=100/num_of_lanes[j],alpha=0.9,c=c)#c=colormap[np.array(y)])
            ax[j][0].set_xlim([0,highway_length* 1000]) #10km
            ax[j][0].set_ylim([-1,num_of_lanes[j]])
            # ax[j].set_title(f"sim {j}")
            ax[j][0].axhline(-0.5, linestyle='-', color='white')
            ax[j][0].axhline(num_of_lanes[j] - 0.5, linestyle='-', color='white')
            ax[j][0].axes.get_yaxis().set_visible(False)
            clearScreen()
            print(f"Animation time: {i/animation_speed:.2f}/{frames/animation_speed}s Real time: {i*interval/1000*animation_speed*reduce_data/60:.2f}/{anim_time/60:.2f}min")
    ani = FuncAnimation(fig, animate, frames=frames, interval=interval, repeat=False)
    if not export_gif_path: plt.show()
    else:
        writergif = PillowWriter(fps=30) 
        ani.save(export_gif_path, writer=writergif)
    return


