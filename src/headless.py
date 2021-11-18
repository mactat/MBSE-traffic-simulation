from sim import *

inflow = 20 #cars per minute
sim_time = 40

scheduler = Scheduler(
    average_drivers_mood = 0.85, #likelihood of driver not accelerating
    num_of_lanes = 4, 
    highway_length = 10, 
    speed_limit = 20, #in km/h
    step_time = 1,
    propotion_of_autonomous = 1)

results,results_dict = scheduler.simulate(sim_time,inflow)

print(f"Results:{results}/{(sim_time)*inflow}")

# scheduler.highway.lanes[0].add_car(Car(60*1000/3600,scheduler.num_of_lanes,lane=0)) # 60km/h
# scheduler.highway.lanes[1].add_car(Car(50*1000/3600,scheduler.num_of_lanes,lane=1,number=1)) # 60km/h
# while(1):
#     input()

#     scheduler.step()
#     print(scheduler.get_state())