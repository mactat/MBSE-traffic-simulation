from classes import  *
import json

'''
That class in the main brain of the simulation.
It takes all parameters of the simulation and produces output.
It will be able to perform whole simulation or go step by step by simulation.
'''
class Scheduler:
    def __init__(self,num_of_lanes, highway_length, speed_limit,step_time) -> None:
        self.num_of_lanes = num_of_lanes
        self.length = highway_length * 1000 # from km to m
        self.speed_limit = speed_limit

        #fix it later
        self.step_time = step_time # in seconds
        self.highway = Highway(speed_limit = self.speed_limit, no_lanes = self.num_of_lanes, length = self.length)
        self.cumulative_results = {}
        self.actual_time = 0

    # simple simulation with one car
    def sim_with_one_car(self, time_of_sim):
        self.highway.lanes[0].add_car(Car(60*1000/3600)) # 60km/h
        self.highway.lanes[1].add_car(Car(50*1000/3600)) # 60km/h
        return self.simulate(time_of_sim)

    # single step which has to be executed in every refresh of the sim
    def step(self):

        #update map
        self.actual_time += 1
        for lane in self.highway.lanes:
            for car in lane.cars:
                # mkae changes in car, as speed, changing lane, etc
                car.refresh(self.step_time)
        #gather the results
        state = self.get_state()
        self.cumulative_results[self.actual_time] = state
        return state

        #add new cars to the map

    # executin multiple steps
    def simulate(self, time_of_sim):
        time_of_sim = time_of_sim * 60 # to seconds
        for i in range(int(time_of_sim/self.step_time)):
            #update map
            self.step()
        return self.cumulative_results

    def get_state(self):
        state = {}
        for lane in self.highway.lanes:
            state[lane.no] = { car.number:car.position for car in lane.cars }
        return state

