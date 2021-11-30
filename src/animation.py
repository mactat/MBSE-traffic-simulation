from numpy.core.defchararray import decode
from sim import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from matplotlib.animation import FFMpegWriter
import matplotlib
import numpy as np
import os


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
    cmap = matplotlib.cm.get_cmap('tab10')
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
                for _,carattributes in  vechile.items():
                    temp_y.append(number)
                    temp_x.append(carattributes["position"])
                    temp_color.append(cmap(carattributes["color"]))  

        X.append(temp_x)
        Y.append(temp_y)
        colors.append(temp_color)
        flow.append(sample["sim_state"]["cars_passed"])
        speed.append(sample["sim_state"]["average_speed"]*3600/1000)
    return X,Y,colors,flow,speed

def lower_samples(sample_list, multiple):
    return [sample for i, sample in enumerate(sample_list) if i%multiple == 0]


def createAnimation(results_list,animation_speed = 10, highway_length=1,num_of_lanes=2,reduce_data=1,export_gif_path=None,names=None):
    # Data extraction
    all_results = [dictToData(results) for results in results_list]
    X_list =      [resultls[0] for resultls in all_results]
    Y_list =      [resultls[1] for resultls in all_results]
    colors_list = [resultls[2] for resultls in all_results]
    flow_list =   [resultls[3] for resultls in all_results]
    speed_list =  [resultls[4] for resultls in all_results]

    X_list =      [lower_samples(X,reduce_data) for X in X_list]
    Y_list =      [lower_samples(Y,reduce_data) for Y in Y_list]
    colors_list = [lower_samples(colors,reduce_data) for colors in colors_list]
    flow_list =   [lower_samples(flow,reduce_data) for flow in flow_list]
    speed_list =  [lower_samples(speed,reduce_data) for speed in speed_list]

    anim_time = len(X_list[0])
    data_q = len(X_list)
    if not names: names = [f"sim{j+1}" for j in range(data_q)]

    fig, ax = plt.subplots(data_q + 2, squeeze=False)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    cmap = matplotlib.cm.get_cmap('tab10')

    interval = int(1000/animation_speed)
    frames = int(anim_time/reduce_data)

    bar_y =     [k+1 for k in range(data_q)]
    bar_color = [cmap(k) for k in range(data_q)]

    # init params
    # Speed plot
    ax[-2][0].set_facecolor("white")
    ax[-2][0].tick_params(axis='y', colors='black')
    ax[-2][0].set_xlabel("Time[s]")
    ax[-2][0].xaxis.label.set_color('black')
    ax[-2][0].set_ylabel("Speed[km/h]")
    ax[-2][0].yaxis.label.set_color('black')

    # bar plot
    ax[-1][0].set_facecolor("white")
    ax[-1][0].tick_params(axis='y', colors='black')
    ax[-1][0].axes.get_yaxis().set_visible(False)
    ax[-1][0].set_title(f"Vechicles passed the highway")
    font = {'family':  'serif', 'color':  'darkred', 'weight': 'bold','size': 10, 'style': 'italic'}

    # scatter plot
    scatter = []   
    for j in range(data_q):
        for k in range(num_of_lanes[j]-1): ax[j][0].axhline(0.5 + k, linestyle='--', color='white')
        ax[j][0].set_xlim([0,highway_length* 1000])
        ax[j][0].set_ylim([-1,num_of_lanes[j]])
        ax[j][0].set_title(names[j])
        ax[j][0].axhline(-0.5, linestyle='-', color='white')
        ax[j][0].axhline(num_of_lanes[j] - 0.5, linestyle='-', color='white')
        ax[j][0].axes.get_yaxis().set_visible(False)
        scatter.append(ax[j][0].scatter([], [], marker="s",s=50/num_of_lanes[j],alpha=0.9,color=[],cmap="tab10"))

    def animate(i):
        ax[-2][0].clear() 
        # Timer
        fig.suptitle(f"Real time: {i/60:.1f}min",x=0.12,fontdict=font)
        
        # Scatter
        for j in range(data_q):
            x = X_list[j][i]
            y = Y_list[j][i]
            xy = np.asarray([x,y])
            c = np.asarray(colors_list[j][i])
            scatter[j].set_offsets(xy.T)
            scatter[j].set_color(c)
            
            # For linear plot
            ax[-2][0].plot(speed_list[j][:i],color=bar_color[-j-1],label=f"sim{j+1}")
        ax[-2][0].set_title(f"Average speed (speed limit - {int(speed_list[0][0]/0.9)} km/h)")
        ax[-2][0].legend(loc='lower left', facecolor="white",fontsize="5")

        # For bar plot
        ax[-1][0].barh(bar_y, [flow[i] for flow in reversed(flow_list)], color=bar_color)
                    # Print status
        if(i % 50 == 0):
            clearScreen()
            print(f"Animation time: {i/animation_speed:.2f}/{frames/animation_speed}s Real time: {i*interval/1000*animation_speed*reduce_data/60:.2f}/{anim_time/60:.2f}min")
    
    ani = FuncAnimation(fig, animate, frames=frames, interval=interval, repeat=False)

    if not export_gif_path: plt.show()
    else:
        writergif = PillowWriter(fps=15) 
        ani.save(export_gif_path, writer=writergif, dpi=150)
        print(f"File:{export_gif_path} saved.")
    return


