from sim import *
from animation import *

'''
This example shows how to run the simulation along with animation
'''


highway_length = 5
num_of_lanes = 4
average_drivers_mood = 0.85
sim_time = 10
inflow = 60 #cars per minute
speed_limit = 110

scheduler = Scheduler(
                        average_drivers_mood = average_drivers_mood ,
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
scheduler.propotion_of_autonomous = 0.6
scheduler.reset()
results3, results_dict3, average_speed3 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

createAnimation(
    [results_dict1, results_dict2, results_dict3],
    animation_speed = 100,
    reduce_data = 1,
    highway_length=highway_length,
    num_of_lanes=[num_of_lanes, num_of_lanes, num_of_lanes],
    export_gif_path = "../static/autonomous8.gif" #if not provided, animation will be shown in the form of plot
    )

print(f"Results without autonomous vehicles:\nFlow: {results1}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed1:.1f}/{speed_limit} km/h.\n")
print(f"Results with only autonomous vehicles:\nFlow: {results2}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed2:.1f}/{speed_limit} km/h.\n")
print(f"Results with 60/40 autonomous vehicles:\nFlow: {results3}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed3:.1f}/{speed_limit} km/h.\n")