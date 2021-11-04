from random import random

'''
That class is responisible for behaviour of the car.
It will be allowed to decided if we shold accelerate brake or change the lane.
The issue is how it will now, what is it's enviroment(other cars on the road)
'''
class Driver:
    def __init__(self, reaction_time, lane_change_behavior=None, exit_behavior=None, breaking_behavior=None):
        self.reaction_time = reaction_time
        self.lane_change_behavior = lane_change_behavior
        self.exit_behavior = exit_behavior
        self.breaking_behavior = breaking_behavior
    
    # move it to choose action
    def switch_lanes(self):
        rand = random()
        if(rand > 0.99): return "left"
        elif(rand < 0.01): return "right"
        else: return False
    
    # Select action based on car env.
    # Action has to be always valid as we are not handeling any other cases
    # Available actions:
    #  * Accelerate - params:
    #  * Brake - params:
    #  * Change lanes - params: [left,right]
    #  * Take an exit
    def choose_action(self,car_env):
        self.front, self.num_of_lanes = car_env
        action = None
        params = (None,None)
        return action, params

'''
This class represents the car. Car itself do not make any decision, it has to ask the driver.
Crutial for this class will be method refresh, which will update the position, speed etc.
'''
class Car:
    def __init__(self, initial_speed, lane,number = 0, acc = 0, breaking = 0):
        self.driver = Driver(reaction_time=0)
        # In meters from the start of the highway
        self.position = 0
        self.number = number
        # For now we are asuuming that cars are just a point, has to be changed later
        self.size = 0

        # Setter would be better
        self.lane = lane
        self.acc = acc

        #In m/s
        self.current_speed = initial_speed
        self.desired_speed = initial_speed
        self.breaking = breaking
    
    # Has to be depended on driver's behaviour, dummy for now
    def refresh(self,time_elapsed,car_env):
        action, params = self.driver.choose_action(car_env) #should return VALID action and parameters
        # Create behaviour based on selected actionS
        self.current_speed = self.desired_speed
        self.position = self.position + self.current_speed*time_elapsed
        lane = self.driver.switch_lanes()
        if(lane): self.switch_lane(lane)

    def switch_lane(self, direction):
        if(direction == 'left' and self.lane != self.driver.num_of_lanes -1): 
            self.lane += 1
            return True
        if(direction == 'right' and self.lane != 0): 
            self.lane -= 1
            return True
        return False


'''
This will be implemented later as it is car with communication device.
'''
class AutonomousCar(Car):
    def __init__(self, radius, delay):
        self.range = radius
        self.delay = delay


'''
Lane is an elementt of the highway. 
It consist of Cars, length and number.
Later we will need to implement lanr for entering the highway.
'''
class Lane:
    def __init__(self, no, length):
        self.no = no
        self.length = length
        # important, it has to be sorted array
        self.cars = []

    # For now assuming that all the cars are commin from the beggining of the highway
    # Later it has to be changed to allow entering cars from the side of the highway    
    def add_car(self,car: Car):
        #check if list is emty or the first car is not on initial position
        if not self.cars or self.cars[0].position != 0 : 
            car.lane = self.no
            self.cars.append(car)

class Highway:
    def __init__(self, no_lanes, speed_limit, length):
        #In meters!
        self.length = length
        self.no_lanes = no_lanes
        self.lanes = [Lane(no = i,length = self.length) for i in range(no_lanes)]
        self.speed_limit = speed_limit
    def render(self):
        for lane in self.lanes:
            for car in lane.cars:
                if(car.lane != lane.no):
                    lane.cars.remove(car)
                    self.lanes[car.lane].cars.append(car)
        
        for lane in self.lanes: lane.cars.sort(key=lambda car:car.position)
    
    # Returns car env position in a form of distance to front, left_front, left_back, right_front, right_back car
    # [              *<------+->            ]
    # [                      o------>*      ]
    # [           *<---------+-->*          ]
    # that will represent what driver is seeing and if he is able to change the lanes etc.
    # Other params:
    #  * num of lanes
    #  * is there an exit
    #  * is it raining
    #  * speed limit

    def get_car_env(self, car_ind, lane_ind):
        # every change here require change in drivers class, to be able to handle new data

        # front
        if car_ind < len(self.lanes[lane_ind].cars) - 1: front = self.lanes[lane_ind].cars[car_ind + 1].position - self.lanes[lane_ind].cars[car_ind].position
        else: front = float('inf')

        #left front

        #left back

        #right front

        #right back
        
        return front, self.no_lanes





