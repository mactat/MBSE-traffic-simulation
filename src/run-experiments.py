from sim import *
import numpy as np
import itertools
from multiprocessing import Pool
import csv


def run_x_simulations(param, variable):
    inflow = 35
    sim_time = 20
    average_drivers_mood = 0.85
    num_of_lanes = 4
    highway_length = 10
    speed_limit = 110
    number_of_runs = 20

    # Determine which parameter is in variable
    if param == "inflow": inflow = variable[1]
    elif param == "num_of_lanes": num_of_lanes = variable[1]
    elif param == "speed_limit": speed_limit = variable[1]

    scheduler = Scheduler(
        num_of_lanes = num_of_lanes,
        highway_length = highway_length,
        speed_limit = speed_limit, #in km/h
        step_time = 1,
        average_drivers_mood = average_drivers_mood, #likelihood of driver not accelerating
        propotion_of_autonomous = variable[0])

    results = 0.0
    average_speed = 0.0
    for i in range(number_of_runs):
        if inflow == 0:
            print("inflow zero")
        r, _, a = scheduler.simulate(sim_time,inflow)
        results += r
        average_speed += a
        scheduler.reset()
    results /= number_of_runs
    average_speed /= number_of_runs

    return variable[0], variable[1], results, average_speed

def inflow_test(a):
    return run_x_simulations("inflow", a)
def lane_test(a):
    return run_x_simulations("num_of_lanes", a)
def speed_test(a):
    return run_x_simulations("speed_limit", a)
def general_test(a):
    return run_x_simulations("", a)





pool = Pool()

#test 1: varying inflow
print("Running test 1: variable propotion_of_autonomous and inflow")
autonomous_range = np.arange(0.0, 1.1, 0.1)
inflow_range = np.arange(10, 70, 10)

test1_input = itertools.product(autonomous_range, inflow_range)
test1_results = pool.map(inflow_test, test1_input)

print("Printing test 1 results")
with open('test1.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(test1_results)

#test 2: varying num of lanes
print("Running test 2: variable propotion_of_autonomous and num_of_lanes")
lane_range = np.arange(1, 10, 1)

test2_input = itertools.product(autonomous_range, lane_range)
test2_results = pool.map(lane_test, test2_input)

print("Printing test 2 results")
with open('test2.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(test2_results)


#test 3: varying speed limit
print("Running test 3: variable propotion_of_autonomous and speed_limit")
speed_range = np.arange(50, 140, 10)

test3_input = itertools.product(autonomous_range, speed_range)
test3_results = pool.map(speed_test, test3_input)

print("Printing test 3 results")
with open('test3.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(test3_results)


#test 4:
print("Running test 4: variable propotion_of_autonomous")
test4_input = itertools.product(autonomous_range, [0])
test4_results = pool.map(general_test, test4_input)

print("Printing test 4 results")
with open('test4.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(test4_results)
