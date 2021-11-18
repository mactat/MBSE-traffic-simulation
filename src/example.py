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
results, results_dict1 = scheduler.sim_with_entry_ramp(sim_time)
scheduler.reset()
scheduler.safe_to_file("simentry")
createAnimation(
    [results_dict1],
    animation_speed= 10,
    reduce_data = 3,
    highway_length=highway_length,
    num_of_lanes=[num_of_lanes,num_of_lanes,num_of_lanes]
   )
"""
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
num_of_lanes = 5
average_drivers_mood = 0.85 #
sim_time = 10
inflow = 8 #cars per minute
speed_limit = 80

scheduler = Scheduler(
                        average_drivers_mood = average_drivers_mood ,
                        num_of_lanes = num_of_lanes, 
                        highway_length = highway_length, 
                        speed_limit = speed_limit, #in km/h
                        step_time = 1) # in sec

results, results_dict1 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)
scheduler.safe_to_file("sim1")

createAnimation(
    [results_dict1],
    animation_speed= 10,
    reduce_data = 1,
    highway_length=highway_length,
    num_of_lanes=[num_of_lanes]
)
"""
print(f"Results: {results}/{(sim_time)*inflow}")