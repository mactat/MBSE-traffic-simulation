from sim import *
import numpy as np
from multiprocessing import Pool

inflow = int(input()) #cars per minute
sim_time = float(input())
average_drivers_mood = float(input())
num_of_lanes = int(input())
highway_length = float(input())
speed_limit = float(input())
number_of_runs = float(input())

def run_x_simulations(autonomous):
    scheduler = Scheduler(
        average_drivers_mood = average_drivers_mood, #likelihood of driver not accelerating
        num_of_lanes = num_of_lanes,
        highway_length = highway_length,
        speed_limit = speed_limit, #in km/h
        step_time = 1,
        propotion_of_autonomous = autonomous)

    results = 0
    average_speed = 0.0
    for i in range(number_of_runs):
        r, _, a = scheduler.simulate(sim_time,inflow)
        results += r
        average_speed += a
        scheduler.reset()
    results /= number_of_runs
    average_speed /= number_of_runs

    return autonomous, results, average_speed


pool = Pool()
results_list = pool.map(run_x_simulations, np.arange(0.0, 1.1, 0.1))

for x in results_list:
    print(x[0], x[1], x[2])


#print(f"Results: {results}/{(sim_time)*inflow} vehicles passed.\nAverage speed: {average_speed:.1f} km/h with speed limit { speed_limit }")


# scheduler.highway.lanes[0].add_car(Car(60*1000/3600,scheduler.num_of_lanes,lane=0)) # 60km/h
# scheduler.highway.lanes[1].add_car(Car(50*1000/3600,scheduler.num_of_lanes,lane=1,number=1)) # 60km/h
# while(1):
#     input()

#     scheduler.step()
#     print(scheduler.get_state())
