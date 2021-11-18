from sim import *
from animation import *

'''
This example shows how to run the simulation along with animation
'''


highway_length = 1
num_of_lanes = 5
average_drivers_mood = 0.90 #
sim_time = 3
inflow = 60 #cars per minute
speed_limit = 90

scheduler = Scheduler(
                        average_drivers_mood = average_drivers_mood ,
                        num_of_lanes = num_of_lanes, 
                        highway_length = highway_length, 
                        speed_limit = speed_limit, #in km/h
                        step_time = 1) # in sec

# Only normal cars
results1, results_dict1 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

# Only outonomous cars
scheduler.propotion_of_autonomous = 1
scheduler.reset()
results2, results_dict2 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

# 50/50
scheduler.propotion_of_autonomous = 0.5
scheduler.reset()
results3, results_dict3 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

createAnimation(
    [results_dict1, results_dict2, results_dict3],
    animation_speed = 1,
    reduce_data = 1,
    highway_length=highway_length,
    num_of_lanes=[num_of_lanes, num_of_lanes, num_of_lanes],
    export_gif_path = "../static/autonomous.gif" #if not provided, animation will be shown in the form of plot
    )

print(f"Results without autonomous: {results1}/{(sim_time)*inflow}")
print(f"Results with only autonomous: {results2}/{(sim_time)*inflow}")
print(f"Results with 50/50: {results3}/{(sim_time)*inflow}")