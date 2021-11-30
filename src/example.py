from matplotlib import animation
from sim import *
from animation import *

'''
This example shows how to run multile simulations along with animation
'''

highway_length =       5
num_of_lanes =         3
average_drivers_mood = 0.85
sim_time =             15
inflow =               45 #cars per minute
speed_limit =          110
propotion_autonomous = 0.3
propotion_of_trucks =  0.2

scheduler = Scheduler(
    average_drivers_mood = average_drivers_mood,
    num_of_lanes =         num_of_lanes, 
    highway_length =       highway_length, 
    speed_limit =          speed_limit, # in km/h
    propotion_of_trucks =  propotion_of_trucks,
    step_time =            1)           # in sec

# For storing output from multiple sims
animation_inp = {"results":[], "lanes":[], "names":[]}

# Normal cars/trucks 80/20
results1, results_dict1, average_speed1 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

# Example of saving to file
scheduler.safe_results_to_file("test")

# Storing output
animation_inp["results"].append(results_dict1)
animation_inp["lanes"].append(scheduler.num_of_lanes)
animation_inp["names"].append(f"Cars/Trucks {int(100*(1 - scheduler.propotion_of_trucks))}/{int(100*scheduler.propotion_of_trucks)}")

# 30/20/50
scheduler.propotion_of_autonomous = propotion_autonomous
scheduler.reset()
results2, results_dict2, average_speed2 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

animation_inp["results"].append(results_dict2)
animation_inp["lanes"].append(scheduler.num_of_lanes)
animation_inp["names"].append(f"Cars/Trucks/Autonomous {int((1 - scheduler.propotion_of_trucks - scheduler.propotion_of_autonomous)*100)}/{int(scheduler.propotion_of_trucks*100)}/{int(100*scheduler.propotion_of_autonomous)}")

# Only outonomous cars
scheduler.propotion_of_autonomous = 1
scheduler.propotion_of_trucks = 0
scheduler.reset()
results3, results_dict3, average_speed3 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

animation_inp["results"].append(results_dict3)
animation_inp["lanes"].append(scheduler.num_of_lanes)
animation_inp["names"].append(f"Only autonomous")

# Autonomous with trucks 80/20
scheduler.propotion_of_autonomous = 0.8
scheduler.propotion_of_trucks = 0.2
scheduler.reset()
results4, results_dict4, average_speed4 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

animation_inp["results"].append(results_dict4)
animation_inp["lanes"].append(scheduler.num_of_lanes)
animation_inp["names"].append(f"Autonomous/Trucks {int(100*scheduler.propotion_of_autonomous)}/{int(100*scheduler.propotion_of_trucks)}")

createAnimation(
    results_list =    animation_inp["results"],
    animation_speed = 100,
    reduce_data =     1,
    highway_length =  highway_length,
    num_of_lanes =    animation_inp["lanes"],
    names =           animation_inp["names"],  # if not provided default
    export_gif_path = f"../static/example.gif" # if not provided, animation will be shown in the form of plot
    )

# Example of printing results 
print(f"Results without autonomous vehicles:\nFlow: {results1}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed1:.1f}/{speed_limit} km/h.\n")
print(f"Results with only autonomous vehicles:\nFlow: {results2}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed2:.1f}/{speed_limit} km/h.\n")
print(f"Results with 60/40 autonomous vehicles:\nFlow: {results3}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed3:.1f}/{speed_limit} km/h.\n")