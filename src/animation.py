from sim import *
import matplotlib.pyplot as plt
from pylab import text
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import matplotlib
import numpy as np
import os
import json
import random

#style
plt.rcParams.update({
    "lines.color":       "white",
    "patch.edgecolor":   "white",
    "text.color":        "black",
    "axes.facecolor":    "black",
    "axes.edgecolor":    "lightgray",
    "axes.labelcolor":   "white",
    "xtick.color":       "black",
    "ytick.color":       "white",
    "grid.color":        "lightgray",
    "figure.facecolor":  "white",
    "figure.edgecolor":  "white",
    "savefig.facecolor": "white",
    "savefig.edgecolor": "black"})


'''
Function for clening the screen, only needed in case of printing simulation in console
'''
def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def dictToData(results):
    
    # Extraction of relevant data for animation. 
    # X and Y position as well as car Color is extracted
    X = []  
    Y = []
    colors = []
    speed = []
    flow = []
    for sample in results["Time"].values():
        # init temps for each time cycle
        temp_x=[]
        temp_y = []
        temp_color = []
        for number,lane in sample["Lanes"].items():
            for vechile in lane.values():
                for id,carattributes in  vechile.items():
                    temp_y.append(number)
                    temp_x.append(carattributes["position"])
                    temp_color.append(carattributes["color"])  
        X.append(temp_x)
        Y.append(temp_y)
        colors.append(temp_color)
        flow.append(sample["sim_state"]["cars_passed"])
        speed.append(sample["sim_state"]["average_speed"]*3600/1000)
    return X,Y,colors,flow,speed

def lower_samples(sample_list, multiple):
    return [sample for i, sample in enumerate(sample_list) if i%multiple == 0]


def createAnimation(results_list,animation_speed = 10, highway_length=10,num_of_lanes=2,reduce_data=10,export_gif_path=None):
    all_results = [dictToData(results) for results in results_list]
    X_list = [resultls[0] for resultls in all_results]
    Y_list = [resultls[1] for resultls in all_results]
    colors_list = [resultls[2] for resultls in all_results]
    flow_list = [resultls[3] for resultls in all_results]
    speed_list = [resultls[4] for resultls in all_results]

    anim_time = len(X_list[0])
    X_list = [lower_samples(X,reduce_data) for X in X_list]
    Y_list = [lower_samples(Y,reduce_data) for Y in Y_list]
    colors_list = [lower_samples(colors,reduce_data) for colors in colors_list]
    flow_list = [lower_samples(flow,reduce_data) for flow in flow_list]
    speed_list = [lower_samples(speed,reduce_data) for speed in speed_list]

    data_q = len(X_list)
    fig, ax = plt.subplots(data_q + 2, squeeze=False)
    plt.xlabel("meters")
    #size_adj = num_of_lanes[0]/100
    #plt.subplots_adjust(bottom=(0.3-size_adj),top=(0.7+size_adj))
    plt.set_cmap('gist_rainbow')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    cmap = matplotlib.cm.get_cmap('tab10')
    manager = plt.get_current_fig_manager()
    #manager.full_screen_toggle()
    interval = int(1000/animation_speed)
    frames = int(anim_time/reduce_data)
    bar_y = [k+1 for k in range(data_q)]
    bar_color = [cmap(k) for k in range(data_q)]
    sim_names = list(reversed([f"sim{k+1}" for k in range(data_q)]))

    
    def animate(i):
        for txt in fig.texts: 
            txt.set_visible(False)
            del txt

        fig.suptitle(f"Real time: {i/60:.1f}min",x=0.12,fontdict={'family':  'serif',
                                                                        'color':  'darkred',
                                                                        'weight': 'bold',
                                                                        'size':   10,
                                                                        'style': 'italic'
                                                                        })
        ax[-2][0].clear()
        for j in range(data_q):
            x = X_list[j][i]
            y = Y_list[j][i]
            c = colors_list[j][i]
            ax[j][0].clear()
            for k in range(num_of_lanes[j]-1): ax[j][0].axhline(0.5 + k, linestyle='--', color='white')

            for z in range(len(x)):
                ax[j][0].scatter(x[z], y[z], marker="s",s=50/num_of_lanes[j],alpha=0.9,c=[cmap(c[z])])

            ax[j][0].set_xlim([0,highway_length* 1000])
            ax[j][0].set_ylim([-1,num_of_lanes[j]])
            ax[j][0].set_title(f"sim{j+1}")
            ax[j][0].axhline(-0.5, linestyle='-', color='white')
            ax[j][0].axhline(num_of_lanes[j] - 0.5, linestyle='-', color='white')
            ax[j][0].axes.get_yaxis().set_visible(False)
            if(j % 100 == 0):
                clearScreen()
                print(f"Animation time: {i/animation_speed:.2f}/{frames/animation_speed}s Real time: {i*interval/1000*animation_speed*reduce_data/60:.2f}/{anim_time/60:.2f}min")

            # For linear plot
            ax[-2][0].plot(speed_list[j][:i],color=bar_color[-j-1],label=f"sim{j+1}")
        ax[-2][0].set_title(f"Average speed (speed limit - {(speed_list[0][0]/0.9):.1f} km/h)")
        ax[-2][0].set_facecolor("white")
        ax[-2][0].tick_params(axis='y', colors='black')
        ax[-2][0].set_xlabel("Time[s]")
        ax[-2][0].set_ylabel("Speed[km/h]")
        ax[-2][0].legend(loc='lower left', facecolor="white",fontsize="6")

        # For bar plot
        ax[-1][0].barh(bar_y, 
                        [flow[i] for flow in reversed(flow_list)], 
                        color=bar_color)
        ax[-1][0].set_facecolor("white")
        ax[-1][0].tick_params(axis='y', colors='black')
        ax[-1][0].set_yticklabels(["0"] + sim_names) # i have no clue why it is a case
        ax[-1][0].set_title(f"Vechicles passed the highway")
    
    ani = FuncAnimation(fig, animate, frames=frames, interval=interval, repeat=False)
    if not export_gif_path: plt.show()
    else:
        writergif = PillowWriter(fps=20) 
        ani.save(export_gif_path, writer=writergif,dpi=200)
    return


