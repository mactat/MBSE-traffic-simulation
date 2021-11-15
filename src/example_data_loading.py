from sim import *
from animation import *

highway_length = 2
num_of_lanes = 7
average_drivers_mood = 0.85 #
sim_time = 4
inflow = 15 #cars per minute
speed_limit = 90

scheduler = Scheduler(
                        average_drivers_mood = average_drivers_mood ,
                        num_of_lanes = num_of_lanes, 
                        highway_length = highway_length, 
                        speed_limit = speed_limit, #in km/h
                        step_time = 1) # in sec

results, results_dict1 = scheduler.simulate(time_of_sim = sim_time, inflow = inflow)

# Exporting results
scheduler.safe_results_to_file("sim1.json")

# Exporting whole scheduler
scheduler.safe_to_file("test.pkl")
#del scheduler

# Importing scheduler
scheduler1 = Scheduler.load_from_file("test.pkl")

assert scheduler1.cars_passed == results
