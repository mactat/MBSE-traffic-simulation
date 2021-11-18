from numpy.lib.function_base import average
from classes import  *
import json
import random

'''
That class in the main brain of the simulation.
It takes all parameters of the simulation and produces output.
It will be able to perform whole simulation or go step by step by simulation.
'''
class Scheduler:
    def __init__(self,num_of_lanes, highway_length, speed_limit,step_time,average_drivers_mood) -> None:
        self.num_of_lanes = num_of_lanes
        self.length = highway_length * 1000 # from km to m
        self.speed_limit = speed_limit*1000/3600
        self.average_drivers_mood = average_drivers_mood

        #fix it later
        self.step_time = step_time # in seconds
        self.highway = Highway(speed_limit = self.speed_limit, no_lanes = self.num_of_lanes, length = self.length)
        self.cumulative_results = {}
        self.actual_time = 0
        self.in_car_counter = 0
        self.cars_passed = 0

    # simple simulation with one car
    def sim_with_two_car(self, time_of_sim):
        slow_car = Car(50 * 1000 / 3600, lane=1, number=self.in_car_counter)
        slow_car.driver.mood = 1
        self.highway.lanes[1].add_car(slow_car)
        self.in_car_counter += 1
        for i in range(10): self.step()
        self.highway.lanes[1].add_car(Car(60 * 1000 / 3600,
                                          lane=1,
                                          number=self.in_car_counter))
        self.in_car_counter += 1
        # self.add_cars(1)
        # for i in range(10): self.step()
        # self.add_cars(1)
        return self.simulate(time_of_sim, 0)

    def sim_with_entry_ramp(self, time_of_sim):
        self.highway.add_entrylane(1000, 1000*0.5)
        print(self.highway.lanes)
        car = Car(50*1000/3600,lane=1, number=self.in_car_counter)
        car.driver.mood = 1
        self.highway.lanes[1].add_car(car)
        self.in_car_counter += 1
        for i in range(10): self.step()
        self.highway.lanes[1].add_car(Car(60*1000/3600,
                                                lane=1,
                                                number=self.in_car_counter))
        self.in_car_counter += 1
        # self.add_cars(1)
        # for i in range(10): self.step()
        # self.add_cars(1)
        return self.simulate(time_of_sim,0)

    def sim_lane_changing(self, time_of_sim, change_lane=False, overtake = False):
  
        if not change_lane and not overtake:

            car1 = Car(50*1000/3600,lane=0, number=self.in_car_counter)
            car1.driver.mood = 1
            self.in_car_counter += 1
            car2 = Car(50*1000/3600,lane=1, number=self.in_car_counter)
            car2.driver.mood = 1
            self.in_car_counter += 1

            self.highway.lanes[0].add_car(car1)
            self.highway.lanes[1].add_car(car2)

        if change_lane and not overtake:
            car1 = Car(55*1000/3600,lane=0, number=self.in_car_counter)
            car1.driver.mood = 1
            self.in_car_counter += 1
            car2 = Car(50*1000/3600,lane=1, number=self.in_car_counter)
            car2.driver.mood = 0.9
            self.in_car_counter += 1
            self.highway.lanes[0].add_car(car1)
            self.highway.lanes[1].add_car(car2)

        if overtake:
            car1 = Car(55*1000/3600,lane=0, number=self.in_car_counter)
            car1.driver.mood = 1
            self.in_car_counter += 1
            car2 = Car(60*1000/3600,lane=0, number=self.in_car_counter)
            car2.driver.mood = 0.9
            self.in_car_counter += 1

            self.highway.lanes[0].add_car(car1)
            for i in range(10): self.step()
            self.highway.lanes[0].add_car(car2)

        return self.simulate(time_of_sim-10,0)

    # single step which has to be executed in every refresh of the sim
    def step(self):

        #update map
        self.actual_time += 1
        for lane_ind,lane in enumerate(self.highway.lanes):
            print(type(lane_ind))
            print(type(lane))
            for car_ind,car in enumerate(lane.cars):
                # gateher info about car env
                car_env = self.highway.get_car_env(car_ind, lane_ind)
                # make changes in car, as speed, changing lane, etc based on env
                car.refresh(self.step_time,car_env)
                if car.position > self.length: 
                    lane.cars.remove(car)
                    self.cars_passed += 1

        self.highway.render()
        #gather the results
        state = self.get_state()
        self.cumulative_results[self.actual_time] = state
        return self.cars_passed,state

    def choose_speed(self):    
        return random.gauss(self.speed_limit/2, 0.1*self.speed_limit) 
    #add new cars to the map
    def add_cars(self,num=1):  
        for i in range(num):
            rand_lane = random.randint(0,self.num_of_lanes-1)
            added = self.highway.lanes[rand_lane].add_car(Car(self.choose_speed()*1000/3600,
                                                lane=rand_lane,
                                                number=self.in_car_counter,
                                                drivers_mood=random.gauss(self.average_drivers_mood, 0.05)))
            if added: self.in_car_counter += 1
    # executin multiple steps
    def simulate(self, time_of_sim, inflow):
        time_of_sim = time_of_sim * 60 # to seconds
        for i in range(int(time_of_sim/self.step_time)):
            #update map
            self.step()
            
            if(inflow and self.actual_time%(int(60/inflow)) == 0): self.add_cars()
        return self.cars_passed, self.cumulative_results
        
    def get_cumulative_state(self):
        return self.cumulative_results

    def get_state(self):
        state = {}
        for lane in self.highway.lanes:
            state[lane.no] = { car.number:car.position for car in lane.cars }
        return state
    def safe_to_file(self, filename):
        out_file = open(f"{ filename }.json", "w") 
        json.dump(self.cumulative_results, out_file, indent = 6) 
        out_file.close() 

    def reset(self):
        self.highway = Highway(speed_limit = self.speed_limit, no_lanes = self.num_of_lanes, length = self.length)
        self.cumulative_results = {}
        self.actual_time = 0
        self.cars_passed = 0

# Debugging
# inflow = 3 #cars per minute
# sim_time = 120
# scheduler = Scheduler(
#     average_drivers_mood = 0.95, #likelihood of driver not accelerating
#     num_of_lanes = 4, 
#     highway_length = 10, 
#     speed_limit = 60, #in km/h
#     step_time = 1) # in sec

# results,results_dict = scheduler.simulate(sim_time,inflow)
# out_file = open("out.json", "w") 
# json.dump(results_dict, out_file, indent = 6) 
# out_file.close() 
# print(f"Results:{results}/{(sim_time-1)*inflow}")


# scheduler.highway.lanes[0].add_car(Car(60*1000/3600,scheduler.num_of_lanes,lane=0)) # 60km/h
# scheduler.highway.lanes[1].add_car(Car(50*1000/3600,scheduler.num_of_lanes,lane=1,number=1)) # 60km/h
# while(1):
#     input()

#     scheduler.step()
#     print(scheduler.get_state())