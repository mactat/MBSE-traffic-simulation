from sim import *
from animation import *

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
# results, results_dict1 = scheduler.sim_lane_changing(sim_time,change_lane=False)
# scheduler.reset()
# results, results_dict2 = scheduler.sim_lane_changing(sim_time,change_lane=True)
# scheduler.reset()
# results, results_dic3 = scheduler.sim_lane_changing(sim_time,change_lane=True,overtake=True)
# scheduler.reset()

# createAnimation(
#     [results_dict1,results_dict2,results_dic3],
#     animation_speed= 10,
#     reduce_data = 3,
#     highway_length=highway_length,
#     num_of_lanes=[num_of_lanes,num_of_lanes,num_of_lanes],
#     export_gif_path = "../static/basecase.gif"
#    )

# ======================= More complicated ====================

highway_length = 2
num_of_lanes = 3
average_drivers_mood = 0.95 #
sim_time = 4
inflow = 40 #cars per minute
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
    animation_speed = 100,
    reduce_data = 1,
    highway_length=highway_length,
    num_of_lanes=[num_of_lanes, num_of_lanes, num_of_lanes],
    export_gif_path = "../static/autonomous.gif" #if not provided, animation will be shown in the form of plot
    )

print(f"Results without autonomous: {results1}/{(sim_time)*inflow}")
print(f"Results with only autonomous: {results2}/{(sim_time)*inflow}")
print(f"Results with 50/50: {results3}/{(sim_time)*inflow}")