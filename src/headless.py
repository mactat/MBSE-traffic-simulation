from sim import *

inflow = int(input()) #cars per minute
sim_time = float(input())
average_drivers_mood = float(input())
num_of_lanes = int(input())
highway_length = float(input())
speed_limit = float(input())
propotion_of_autonomous = float(input())

scheduler = Scheduler(
    average_drivers_mood = average_drivers_mood, #likelihood of driver not accelerating
    num_of_lanes = num_of_lanes, 
    highway_length = highway_length, 
    speed_limit = speed_limit, #in km/h
    step_time = 1,
    propotion_of_autonomous = propotion_of_autonomous)

results, results_dict, average_speed = scheduler.simulate(sim_time,inflow)

print(f"Results: {results}/{(sim_time)*inflow} vehicles passed.\nAverage speed: {average_speed:.1f} km/h with speed limit { speed_limit }")


# scheduler.highway.lanes[0].add_car(Car(60*1000/3600,scheduler.num_of_lanes,lane=0)) # 60km/h
# scheduler.highway.lanes[1].add_car(Car(50*1000/3600,scheduler.num_of_lanes,lane=1,number=1)) # 60km/h
# while(1):
#     input()

#     scheduler.step()
#     print(scheduler.get_state())