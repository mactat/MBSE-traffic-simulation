from sim import *
from animation import *

'''
This example shows how to run the simulation along with animation
'''

# ====================== examples =====================
highway_length = 7
num_of_lanes = 4
average_drivers_mood = 0.85 #
sim_time = 20
inflow = 4 #cars per minute
speed_limit = 60
scheduler = Scheduler(
                        average_drivers_mood = average_drivers_mood ,
                        num_of_lanes = num_of_lanes, 
                        highway_length = highway_length, 
                        speed_limit = speed_limit, #in km/h
                        step_time = 1) # in sec

# # ========================= Base cases ============================
results, results_dict1 = scheduler.sim_lane_changing(sim_time,change_lane=False)
scheduler.reset()
results, results_dict2 = scheduler.sim_lane_changing(sim_time,change_lane=True)
scheduler.reset()
results, results_dic3 = scheduler.sim_lane_changing(sim_time,change_lane=True,overtake=True)
scheduler.reset()

createAnimation(
    [results_dict1,results_dict2,results_dic3],
    animation_speed= 10,
    reduce_data = 3,
    highway_length=highway_length,
    num_of_lanes=[num_of_lanes,num_of_lanes,num_of_lanes]
   )

# ======================= More complicated ====================

highway_length = 1
num_of_lanes = 3
average_drivers_mood = 0.90 #
sim_time = 2
inflow = 40 #cars per minute
speed_limit = 110

scheduler = Scheduler(
                        average_drivers_mood = average_drivers_mood ,
                        num_of_lanes = num_of_lanes, 
                        highway_length = highway_length, 
                        speed_limit = speed_limit, #in km/h
                        step_time = 1) # in sec

# Only normal cars
results1, results_dict1, average_speed1 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

# Only outonomous cars
scheduler.propotion_of_autonomous = 1
scheduler.reset()
results2, results_dict2, average_speed2 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

# 50/50
scheduler.propotion_of_autonomous = 0.5
scheduler.reset()
results3, results_dict3, average_speed3 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

createAnimation(
    [results_dict1, results_dict2, results_dict3],
    animation_speed = 1,
    reduce_data = 1,
    highway_length=highway_length,
    num_of_lanes=[num_of_lanes, num_of_lanes, num_of_lanes],
    export_gif_path = "../static/autonomous2.gif" #if not provided, animation will be shown in the form of plot
    )


print(f"Results without autonomous vehicles:\nFlow: {results1}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed1:.1f}/{speed_limit} km/h.\n")
print(f"Results with only autonomous vehicles:\nFlow: {results2}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed2:.1f}/{speed_limit} km/h.\n")
print(f"Results with 50/50 autonomous vehicles:\nFlow: {results3}/{(sim_time)*inflow} vehicles passed the highway.\nAverage speed: {average_speed3:.1f}/{speed_limit} km/h.\n")