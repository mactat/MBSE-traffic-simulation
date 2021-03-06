from numpy.lib.function_base import average
import numpy as np
from classes import  *
import json
import random
import pickle

'''
That class in the main brain of the simulation.
It takes all parameters of the simulation and produces output.
It will be able to perform whole simulation or go step by step by simulation.
'''
class Scheduler:
    def __init__(self,num_of_lanes, highway_length, speed_limit,step_time, average_drivers_mood, propotion_of_autonomous=0, propotion_of_trucks=0) -> None:
        self.num_of_lanes = num_of_lanes
        self.length = highway_length * 1000 # from km to m
        self.speed_limit = speed_limit*1000/3600
        self.average_drivers_mood = average_drivers_mood
        self.propotion_of_autonomous = propotion_of_autonomous
        self.propotion_of_trucks = propotion_of_trucks
        self.step_time = step_time # in seconds
        self.highway = Highway(speed_limit = self.speed_limit, no_lanes = self.num_of_lanes, length = self.length)
        self.cumulative_results = {"Time":{}}
        self.actual_time = 0
        self.in_car_counter = 0
        self.cars_passed = 0
        self.samples = 0
        self.average_speed = 0.9*self.speed_limit

    def update_average_speed(self,speed):
        self.samples += 1
        self.average_speed = (self.average_speed * (self.samples - 1) + speed)/self.samples

    # single step which has to be executed in every refresh of the sim
    def step(self):
        # Increase clock
        self.actual_time += 1

        # Decide on action
        for lane_ind,lane in enumerate(self.highway.lanes):
            for car_ind,car in enumerate(lane.cars):
                # Gateher info about car env
                car_env = self.highway.get_car_env(car_ind, lane_ind, type(car))
                self.update_average_speed(car.current_speed)
                # Make changes in car, as speed, changing lane, etc based on env
                car.driver_decide(self.step_time,car_env)

        # Invoke action
        for lane_ind,lane in enumerate(self.highway.lanes):
            for car_ind,car in enumerate(lane.cars):

                # Gateher info about car env
                car_env = self.highway.get_car_env(car_ind, lane_ind)

                # Make changes in car, as speed, changing lane, etc based on env
                if type(car) == Car or type(car) == Truck:
                    car.take_action(self.step_time)
                elif type(car) == AutonomousCar:
                    autonomous_car_env = self.highway.get_autonomous_car_env(car_ind, lane_ind)
                    car.take_action(self.step_time, car_env, autonomous_car_env)
                
                # Evaluate if car passed the element of the highway
                if car.position > self.length: 
                    lane.cars.remove(car)
                    self.cars_passed += 1

        # Update positions of the cars
        self.highway.render()


        #gather the results    
        state = self.get_state()
        self.cumulative_results["Time"][self.actual_time] = state

        return self.cars_passed,state


    # Chossing random speed from gausian distribution
    def choose_speed(self,truck=False):    
        if truck:
            speed = random.gauss(0.7 * self.speed_limit, 0.1*self.speed_limit) 
        else:
            speed = random.gauss(0.9 * self.speed_limit, 0.1*self.speed_limit) 
        if speed > self.speed_limit: speed = self.speed_limit
        return speed

    # Add new vehicles to the map
    def add_vehicles(self,num=1):  
        for i in range(num):
            rand_lane = random.randint(0,self.num_of_lanes-1)
            rand_vehicle = self.get_random_vehicle(rand_lane)
            added = self.highway.lanes[rand_lane].add_car(rand_vehicle)
            if added: self.in_car_counter += 1

    # Execute multiple steps
    def simulate(self, time_of_sim, inflow):
        time_of_sim = time_of_sim * 60 # to seconds
        for i in range(int(time_of_sim/self.step_time)):

            #update map
            self.step()
            if(inflow and self.actual_time%(int(60/inflow)) == 0): self.add_vehicles()
        return self.cars_passed, self.cumulative_results, self.average_speed * 3.6
        
    def get_cumulative_state(self):
        return self.cumulative_results

    def get_random_vehicle(self, lane):
        vehicle_type = np.random.choice([Car,AutonomousCar, Truck], 1, p=[1-(self.propotion_of_trucks + self.propotion_of_autonomous),self.propotion_of_autonomous,self.propotion_of_trucks])
        if vehicle_type == Car:
            return Car(self.choose_speed(),
                        lane = lane,
                        number = self.in_car_counter,
                        drivers_mood = random.gauss(self.average_drivers_mood, 0.05))
        elif vehicle_type == AutonomousCar:
            return AutonomousCar(self.choose_speed(),
                                    lane = lane,
                                    number = self.in_car_counter,
                                    drivers_mood = 0,
                                    radius = 1000, 
                                    delay = 0)
        elif vehicle_type == Truck:
            return Truck(self.choose_speed(True),
                                    lane = lane,
                                    number = self.in_car_counter,
                                    drivers_mood = 0.9 
                                    )
    def get_state(self):
        state ={"Lanes":{},"sim_state":{}}
        for lane in self.highway.lanes:
               state["Lanes"][lane.no] = { "IDs":{vechile.number:{     
                                                   "type":type(vechile).__name__,  # TODO: Fix when type is introduced 
                                                   "position":vechile.position, 
                                                   "speed":vechile.current_speed,  
                                                   "color":vechile.color }
                                                    for vechile in lane.cars}  # TODO: Make color dependent on car type 
                                                   }

        state["sim_state"] = {"cars_passed": self.cars_passed,
                                "average_speed": self.average_speed}

        return state

    def safe_results_to_file(self, filename):
        out_file = open(f"{ filename }.json", "w") 
        json.dump(self.cumulative_results, out_file, indent = 6) 
        out_file.close() 

    def safe_to_file(self, filepath="scheduler.pkl"):
        with open(filepath, 'wb') as file:  # Overwrites any existing file.
            pickle.dump(self, file)
            print(f"Scheduler saved to {filepath}")
            
    @staticmethod        
    def load_from_file(filepath="scheduler.pkl"):
        with open(filepath, 'rb') as file:  # Overwrites any existing file.
            scheduler = pickle.load(file)
            print(f"Scheduler loaded from {filepath}")
        return scheduler
    
    # Reset scheduler state 
    def reset(self):
        self.highway = Highway(speed_limit = self.speed_limit, no_lanes = self.num_of_lanes, length = self.length)
        self.cumulative_results = {"Time":{}}
        self.actual_time = 0
        self.cars_passed = 0
        self.average_speed = 0.9*self.speed_limit
        self.samples = 0