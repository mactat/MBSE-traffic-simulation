from classes import *
from sim import *
from animation import *

def sim_lane_changing(scheduler, time_of_sim, change_lane=False, overtake = False, entrylane =  False):

    if entrylane:
        scheduler.highway.add_entrylane(1000, 1000)
        car = Car(50 * 1000 / 3600, lane=1, number=scheduler.in_car_counter)
        car.driver.mood = 1
        scheduler.highway.lanes[1].add_car(car)
        scheduler.in_car_counter += 1
        for i in range(10): scheduler.step()
        scheduler.highway.lanes[1].add_car(Car(60 * 1000 / 3600,
                                          lane=1,
                                          number=scheduler.in_car_counter))
        scheduler.in_car_counter += 1
        car2 = Car(50 * 1000 / 3600, lane=1, number=scheduler.in_car_counter)
        car2.driver.mood = 1
        scheduler.in_car_counter += 1
        scheduler.highway.lanes[3].add_car(car2)
        car3 = Car(50 * 1000 / 3600, lane=1, number=scheduler.in_car_counter)
        car3.driver.mood = 1
        scheduler.in_car_counter += 1
        scheduler.highway.lanes[0].add_car(car3)

    if not change_lane and not overtake and not entrylane:

        car1 = Car(int(50*1000/3600),lane=0, number=scheduler.in_car_counter)
        car1.driver.mood = 1
        scheduler.in_car_counter += 1
        car2 = Car(int(50*1000/3600),lane=1, number=scheduler.in_car_counter)
        car2.driver.mood = 1
        scheduler.in_car_counter += 1

        scheduler.highway.lanes[0].add_car(car1)
        scheduler.highway.lanes[1].add_car(car2)
        for i in range(10): scheduler.step()

    if change_lane and not overtake and not entrylane:
        car1 = Car(60*1000/3600,lane=0, number=scheduler.in_car_counter)
        car1.driver.mood = 1
        scheduler.in_car_counter += 1
        car2 = Car(50*1000/3600,lane=1, number=scheduler.in_car_counter)
        car2.driver.mood = 0.9
        scheduler.in_car_counter += 1
        scheduler.highway.lanes[0].add_car(car1)
        scheduler.highway.lanes[1].add_car(car2)
        for i in range(10): scheduler.step()

    if overtake and not entrylane:
        car1 = Car(55*1000/3600,lane=0, number=scheduler.in_car_counter)
        car1.driver.mood = 1
        scheduler.in_car_counter += 1
        car2 = Car(70*1000/3600,lane=0, number=scheduler.in_car_counter)
        car2.driver.mood = 0.9
        scheduler.in_car_counter += 1

        scheduler.highway.lanes[0].add_car(car1)
        for i in range(10): scheduler.step()
        scheduler.highway.lanes[0].add_car(car2)

    return scheduler.simulate(time_of_sim - 10/60,inflow=0)


# ====================== examples =====================
highway_length = 10
num_of_lanes = 3
average_drivers_mood = 0.85 #
sim_time = 11
inflow = 4 #cars per minute
speed_limit = 60

scheduler = Scheduler(
                        average_drivers_mood = average_drivers_mood ,
                        num_of_lanes = num_of_lanes, 
                        highway_length = highway_length, 
                        speed_limit = speed_limit, #in km/h
                        step_time = 1) # in sec

# ========================= Base cases ============================
results, results_dict0, average_speed0 = sim_lane_changing(scheduler,sim_time,entrylane=True)
scheduler.reset()
results, results_dict1, average_speed1 = sim_lane_changing(scheduler,sim_time,change_lane=False)
scheduler.reset()
results, results_dict2, average_speed2 = sim_lane_changing(scheduler,sim_time,change_lane=True)
scheduler.safe_results_to_file("test")
scheduler.reset()
results, results_dict3, average_speed3 = sim_lane_changing(scheduler,sim_time,change_lane=True,overtake=True)
scheduler.reset()

createAnimation(
    [results_dict1, results_dict2, results_dict3],
    animation_speed = 1,
    reduce_data = 4,
    highway_length = highway_length,
    num_of_lanes = [num_of_lanes, num_of_lanes, num_of_lanes],
    export_gif_path = "../static/basecase.gif"
   )