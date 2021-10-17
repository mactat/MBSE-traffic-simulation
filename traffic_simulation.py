import random
from time import sleep
import os
import numpy as np

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Lane:
    def __init__(self,length) -> None:
        self.length = length
        self.mock = self.length * [' ']
        self.num_of_cars_passed = 0

    def __repr__(self) -> str:
        printable_mock = map(str,self.mock)
        return f'|{"".join(printable_mock)}|'
    

    #car is coming to the road    
    def addCar(self,car):
        if self.mock[0] == ' ':
            self.mock[0] = car
            return True
        else: return False

    def step(self):
        for i in range(self.length):
            placeholder = self.mock[-i-1]
            # if there is a car
            if placeholder != ' ':
                #update parameter - accelerate or break or whatever
                placeholder.update()
                # if after next jump it will be further than the road itself
                if(placeholder.current_speed - i > -2): 
                    self.num_of_cars_passed += 1
                    self.mock[-i-1] = ' '
                #for one elif(   self.mock[placeholder.current_speed - i + 1] == ' '):
                #it has to have a clear road to jump for number of units == speed
                elif(self.mock[(-i):(placeholder.current_speed - i + 2)] == (placeholder.current_speed+2)*[' ']):  
                    self.mock[placeholder.current_speed - i + 1] = placeholder
                    self.mock[-i-1] = ' '
                

class Car:
    def __init__(self,average_speed,speed_std) -> None:
        self.average_speed = average_speed
        self.speed_std = speed_std
        self.update()
    def __repr__(self) -> str:
        return '*'
    def update(self):
        np.random.seed()
        self.current_speed = int(np.random.normal(loc=self.average_speed ,scale=self.speed_std,size=1))
        if(self.current_speed < 0): self.current_speed =0
        
class Scheduler:
    def __init__(self,num_of_lanes,average_speed,average_speed_std,speed_std,car_freq,sim_time,sim_speed) -> None:
        self.num_of_lanes = num_of_lanes
        self.average_speed = average_speed
        self.average_speed_std = average_speed_std
        self.speed_std = speed_std
        self.car_freq = car_freq # number of cars coming per time unit
        self.lanes = [ Lane(150) for _ in range(self.num_of_lanes)] #change the lenmgth later

        #for later
        self.simulation_time = sim_time # sec
        self.refresh_freq = 1/sim_speed # 1/sec
    
    def printSim(self):
        for lane in self.lanes: print(lane)

    def result(self):
        cars_passed = [lane.num_of_cars_passed for lane in self.lanes] 
        print(f"Cars passed: {sum(cars_passed)}")
        return sum(cars_passed)

    def generateRandCar(self):
        np.random.seed()
        init_speed = int(np.random.normal(loc=self.average_speed ,scale=self.average_speed_std,size=1)) #something wrong here
        if(init_speed < 0): init_speed =0
        rand_car = Car(init_speed,self.speed_std) # change to given speed and a std
        return rand_car
    def getRandomLane(self):
        np.random.seed()
        return random.randint(0,self.num_of_lanes-1)
    def step(self):
        #update map
        for lane in self.lanes: lane.step()
        for _ in range(self.car_freq): self.lanes[self.getRandomLane()].addCar(self.generateRandCar())

    def simulate(self):
        for i in range(int(self.simulation_time/self.refresh_freq)):
            self.step()
            clearScreen()    
            self.printSim()
            results = self.result()
            print(f"Time of simulation {i*self.refresh_freq:0.1f}/{self.simulation_time}")
            sleep(self.refresh_freq)
        return results
#tests
car1 = Car(100,5)
print(f"Car: {car1}")
lane = Lane(50)
lane.addCar(car1)
print(f"Lane: {lane}")
print("====================== Simulation ======================")

scheduler = Scheduler(
    num_of_lanes =      5,
    average_speed =     8,
    average_speed_std = 10,
    speed_std =         3,
    car_freq =          4,
    sim_time =          20,
    sim_speed =         10
    )

results1 = scheduler.simulate()


scheduler = Scheduler(
    num_of_lanes =      5,
    average_speed =     8,
    average_speed_std = 0,
    speed_std =         0,
    car_freq =          4,
    sim_time =          20,
    sim_speed =         10
    )
    
results2 = scheduler.simulate()
print(f"Results for simulation 1: {results1}. Result for simulation 2: {results2}")