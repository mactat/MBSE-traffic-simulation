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
    def __init__(self,num_of_lanes, highway_length, speed_limit,step_time, average_drivers_mood, propotion_of_autonomous=0) -> None:
        self.num_of_lanes = num_of_lanes
        self.length = highway_length * 1000 # from km to m
        self.speed_limit = speed_limit*1000/3600
        self.average_drivers_mood = average_drivers_mood
        self.propotion_of_autonomous = propotion_of_autonomous
        self.step_time = step_time # in seconds
        self.highway = Highway(speed_limit = self.speed_limit, no_lanes = self.num_of_lanes, length = self.length)
        self.cumulative_results = {}
        self.actual_time = 0
        self.in_car_counter = 0
        self.cars_passed = 0
        self.samples = 0
        self.average_speed = 0

    def update_average_speed(self,speed):
        self.samples += 1
        self.average_speed = (self.average_speed * (self.samples - 1) + speed)/self.samples
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
        self.highway.add_entrylane(1000, 1000)
        car = Car(50*1000/3600,lane=1, number=self.in_car_counter)
        car.driver.mood = 1
        self.highway.lanes[1].add_car(car)
        self.in_car_counter += 1
        for i in range(10): self.step()
        self.highway.lanes[1].add_car(Car(60*1000/3600,
                                                lane=1,
                                                number=self.in_car_counter))
        self.in_car_counter += 1
        car2 = Car(50 * 1000 / 3600, lane=1, number=self.in_car_counter)
        car2.driver.mood = 1
        self.in_car_counter += 1
        self.highway.lanes[4].add_car(car2)
        car3 = Car(50 * 1000 / 3600, lane=1, number=self.in_car_counter)
        car3.driver.mood = 1
        self.in_car_counter += 1
        self.highway.lanes[0].add_car(car3)
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
        # Increase clock
        self.actual_time += 1

        # Decide on action
        for lane_ind,lane in enumerate(self.highway.lanes):
            for car_ind,car in enumerate(lane.cars):
                # Gateher info about car env
                car_env = self.highway.get_car_env(car_ind, lane_ind)
                self.update_average_speed(car.current_speed)
                # Make changes in car, as speed, changing lane, etc based on env
                car.driver_decide(self.step_time,car_env)

        # Invoke action
        for lane_ind,lane in enumerate(self.highway.lanes):
            for car_ind,car in enumerate(lane.cars):

                # Gateher info about car env
                car_env = self.highway.get_car_env(car_ind, lane_ind)

                # Make changes in car, as speed, changing lane, etc based on env
                if type(car) == Car:
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

        # Save information
        state = self.get_state()
        self.cumulative_results[self.actual_time] = state
        return self.cars_passed, state

    # Chossing random speed from gausian distribution
    def choose_speed(self):    
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
        vehicle_type = np.random.choice([Car, AutonomousCar], 1, p=[1-self.propotion_of_autonomous,self.propotion_of_autonomous])
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
    def get_state(self):
        state = {}
        for lane in self.highway.lanes:
            state[lane.no] = { car.number:car.position for car in lane.cars }
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
        self.cumulative_results = {}
        self.actual_time = 0
        self.cars_passed = 0
        self.average_speed = 0
        self.samples = 0