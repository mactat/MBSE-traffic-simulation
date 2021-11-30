from sim import *
from animation import *

'''
This example shows how to run the simulation along with animation
'''


highway_length =       5
num_of_lanes =         2
average_drivers_mood = 0.85
sim_time =             15
inflow =               20 #cars per minute
speed_limit =          90
propotion_autonomous = 0.3

scheduler = Scheduler(
                        average_drivers_mood = average_drivers_mood,
                        num_of_lanes = num_of_lanes, 
                        highway_length = highway_length, 
                        speed_limit = speed_limit, # in km/h
                        step_time = 1) # in sec

# Only normal cars
results1, results_dict1, average_speed1 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)
scheduler.safe_results_to_file("test")

# Only outonomous cars
scheduler.propotion_of_autonomous = 1
scheduler.reset()
results2, results_dict2, average_speed2 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

# 50/50
scheduler.propotion_of_autonomous = propotion_autonomous
scheduler.reset()
results3, results_dict3, average_speed3 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

createAnimation(
    [results_dict1, results_dict2, results_dict3],
    animation_speed = 100,
    reduce_data = 1,
    highway_length = highway_length,
    num_of_lanes = [num_of_lanes, num_of_lanes, num_of_lanes],
    names = ["Not autonomous", "Fully autonomous", f"{int(propotion_autonomous*100)}/{int((100-propotion_autonomous*100))}"], # if not profided default
    export_gif_path = f"../static/l_{num_of_lanes}_a_{int(propotion_autonomous*100)}_m_{int(average_drivers_mood*100)}.gif" #if not provided, animation will be shown in the form of plot
    )

print(f"Results without autonomous vehicles:\nFlow: {results1}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed1:.1f}/{speed_limit} km/h.\n")
print(f"Results with only autonomous vehicles:\nFlow: {results2}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed2:.1f}/{speed_limit} km/h.\n")
print(f"Results with 60/40 autonomous vehicles:\nFlow: {results3}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed3:.1f}/{speed_limit} km/h.\n")