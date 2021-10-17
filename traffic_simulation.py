import random
from time import sleep
import os
import numpy as np
import json
import matplotlib.pyplot as plt
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
    def lanesToJson(self):
        res_dict = {}
        for num_lane,lane in enumerate(self.lanes):
            res_dict[num_lane] = []
            for num_spac, space in enumerate(lane.mock):
                if space != ' ':
                    res_dict[num_lane].append(num_spac)
        return res_dict

    def result(self):
        cars_passed = [lane.num_of_cars_passed for lane in self.lanes] 
        print(f"Cars passed: {sum(cars_passed)}")
        return sum(cars_passed), self.lanesToJson()
    

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

    def simulate(self,print_sim=True):
        cumulative_results = []
        for i in range(int(self.simulation_time/self.refresh_freq)):
            self.step()
            clearScreen()    
            if print_sim: self.printSim()
            cars_passed, result = self.result()
            print(f"Time of simulation {i*self.refresh_freq:0.1f}/{self.simulation_time}")
            sleep(self.refresh_freq)
            cumulative_results.append(result)
        return cars_passed,json.dumps(cumulative_results)
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
    sim_time =          1,
    sim_speed =         100
    )

flow1, results1 = scheduler.simulate(print_sim=False)

scheduler = Scheduler(
    num_of_lanes =      5,
    average_speed =     8,
    average_speed_std = 0,
    speed_std =         0,
    car_freq =          4,
    sim_time =          1,
    sim_speed =         100
    )
    
flow2, results2 = scheduler.simulate(print_sim=False)
print(f"Results for simulation 1: {flow1}. Result for simulation 2: {flow2}")
# print(results1)

#try animation in matplotlib
from matplotlib.animation import FuncAnimation

def jsonToData(results):
    results = json.loads(results)
    X=[[single_val for key,val in sample.items() for single_val in val] for sample in results]
    Y=[[int(key)   for key,val in sample.items() for single_val in val] for sample in results]
    return X,Y

def createAnimation(X_list,Y_list):
    data_q = len(X_list)
    fig, ax = plt.subplots(data_q)
    #plt.subplots_adjust(bottom=0.5,top=0.6)
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    colormap = np.array(['k','b','y','g','r'])

    def animate(i):
        for j in range(data_q):
            x = X_list[j][i]
            y = Y_list[j][i]
            ax[j].clear()
            ax[j].scatter(x, y, marker="s",c=colormap[np.array(y)])
            ax[j].set_xlim([0,150])
            ax[j].set_ylim([-1,5])
    ani = FuncAnimation(fig, animate, frames=len(X1), interval=50, repeat=False)
    plt.show()

X1,Y1 = jsonToData(results1)
X2,Y2 = jsonToData(results2)

createAnimation([X1,X2],[Y1,Y2])
