import math
from random import random

'''
That class is responisible for behaviour of the car.
It will be allowed to decided if we shold accelerate brake or change the lane.
The issue is how it will now, what is it's enviroment(other cars on the road)
'''


class Driver:
    def __init__(self, reaction_time, mood=0.95, lane_change_behavior=None, exit_behavior=None, breaking_behavior=None):
        self.reaction_time = reaction_time
        self.lane_change_behavior = lane_change_behavior
        self.exit_behavior = exit_behavior
        self.breaking_behavior = breaking_behavior
        self.mood = mood

    # move it to choose action
    def switch_lanes(self, left_back, right_back, left_front, right_front):  # params here
        rand = self.random_mood()
        # do we want
        if (rand > 0.5):
            if (left_back > self.speed_limit and left_front > 20): return "left"
        elif (rand < 0.2):
            if (right_back > self.speed_limit and right_front > 20): return "right"
        else:
            return False

    # Select action based on car env.
    # Action has to be always valid as we are not handeling any other cases
    # Available actions:
    #  * Accelerate - params:
    #  * Brake - params:
    #  * Change lanes - params: [left,right]
    #  * Take an exit
    def random_mood(self):
        return random()

    def choose_action(self, car_env):
        self.front, self.num_of_lanes, self.current_speed, self.speed_limit, left_back, right_back, left_front, right_front, self.frontSpeed = car_env

        # check if switching lane is possible
        switch_lane = self.switch_lanes(left_back, right_back, left_front, right_front)
        #Variables for (de)acceleration
        # *Delta v = Difference in speed of car infront and current car
        # * t = reaction time
        # * s0 = Desired minimum distance between cars
        # * si = Distance to car in front
        # * v = Current speed of car
        # * ai = Max acceleration of car, taken from average acceleration in m/s^2 of cars
        # * b = Comfortable deaccleration of car, taken from google search
        # * v0 = desired speed of car, set as the speed limit
        deltav = self.current_speed - self.frontSpeed
        t = self.reaction_time
        s0 = 3
        si = self.front
        v = self.current_speed
        ai = 3.6
        b = 3.6
        v0 = self.speed_limit

        if (self.current_speed * 1 > self.front):
            if switch_lane:
                action = "change_lane"
                params = {"direction": switch_lane}
            else:
                a = ai * (1 - (v / v0) ** 4) - ai * (
                            ((s0 + v * t) / si) + ((v * deltav) / (2 * si * math.sqrt(ai * b)))) ** 2

                adjust = (self.current_speed - self.front / 1) + 10  # adjust
                if (self.current_speed - adjust) < 0: adjust = self.current_speed
                action = "brake"
                params = {"value": a}

        elif (self.front > self.speed_limit + 20 and self.random_mood() > self.mood):
            # to be changed to real formula
            adjust = 0.1 * self.speed_limit / 3.6
            a = ai * (1-(v/v0)**4)

            #if (self.frontSpeed <=0):
              #  a = 3.6 * 1 - (self.current_speed / self.speed_limit)**3 + -3.6 * ((3 + self.current_speed * self.reaction_time) / self.frontSpeed +
                 #        ((self.current_speed * self.frontSpeed) / 2 * self.front * math.sqrt(3.6 * 3.6)))
            if (self.current_speed + adjust) > self.speed_limit: adjust = self.speed_limit - self.current_speed

            action = "accelerate"
            params = {"value": a}
        # params = {"value":adjust}

        # lean towards right behaviour
        elif (switch_lane == 'right' and self.random_mood() > 0.95):
            action = "change_lane"
            params = {"direction": "right"}
        else:
            action = None
            params = {}

        return action, params


'''
This class represents the car. Car itself do not make any decision, it has to ask the driver.
Crutial for this class will be method refresh, which will update the position, speed etc.
'''


class Car:
    def __init__(self, initial_speed, lane, drivers_mood=0.95, number=0, acc=0, breaking=0):
        self.driver = Driver(reaction_time=0, mood=drivers_mood)
        # In meters from the start of the highway
        self.position = 0
        self.number = number
        # For now we are asuuming that cars are just a point, has to be changed later
        self.size = 0

        # Setter would be better
        self.lane = lane
        self.acc = acc

        # In m/s
        self.current_speed = initial_speed
        self.desired_speed = initial_speed
        self.breaking = breaking

    # Has to be depended on driver's behaviour, dummy for now
    def refresh(self, time_elapsed, car_env):
        # chaange the way we define env
        front, num_of_lanes, self.speed_limit, left_back, right_back, left_front, right_front, frontSpeed = car_env
        car_env = front, num_of_lanes, self.current_speed, self.speed_limit, left_back, right_back, left_front, right_front, frontSpeed

        action, params = self.driver.choose_action(car_env)  # should return VALID action and parameters
        # Create behaviour based on selected actions
        if action == 'accelerate':
            self.current_speed = self.current_speed + params["value"]


        if action == 'brake':
            self.current_speed += params["value"]
            if(self.current_speed  <= 0):
                self.current_speed = 0

        if action == 'change_lane':
            self.switch_lane(params["direction"])

        self.position = self.position + self.current_speed * time_elapsed

    # chcking validity can be moved to driver
    def switch_lane(self, direction):
        if (direction == 'left' and self.lane != self.driver.num_of_lanes - 1):
            self.lane += 1
            return True
        if (direction == 'right' and self.lane != 0):
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
    def add_car(self, car: Car):
        # check if list is emty or the first car is not on initial position
        if not self.cars or self.cars[0].position != 0:
            car.lane = self.no
            self.cars.insert(0, car)
            return True
        else:
            return False


class Highway:
    def __init__(self, no_lanes, speed_limit, length):
        # In meters!
        self.length = length
        self.no_lanes = no_lanes
        self.lanes = [Lane(no=i, length=self.length) for i in range(no_lanes)]
        self.speed_limit = speed_limit

    def render(self):
        for lane in self.lanes:
            for car in lane.cars:
                if (car.lane != lane.no):
                    lane.cars.remove(car)
                    self.lanes[car.lane].cars.append(car)

        for lane in self.lanes: lane.cars.sort(key=lambda car: car.position)

    # Returns car env position in a form of distance to front, left_front, left_back, right_front, right_back car
    # [              *<------+->*           ]
    # [                      o------>*      ]
    # [           *<---------+-->*          ]
    # that will represent what driver is seeing and if he is able to change the lanes etc.
    # Other params:
    #  * num of lanes
    #  * is there an exit - later
    #  * is it raining - later
    #  * speed limit - later

    def get_car_env(self, car_ind, lane_ind):
        # every change here require change in drivers class, to be able to handle new data

        # front and front speed
        global frontSpeed
        if car_ind < len(self.lanes[lane_ind].cars) - 1:
            front = self.lanes[lane_ind].cars[car_ind + 1].position - self.lanes[lane_ind].cars[car_ind].position
            frontSpeed = self.lanes[lane_ind].cars[car_ind + 1].current_speed
        else:
            front = float('inf')
            frontSpeed = 0

        my_position = self.lanes[lane_ind].cars[car_ind].position

        # left
        left_front = float("Inf")
        right_front = float("Inf")
        left_back = float("Inf")
        right_back = float("Inf")

        if lane_ind < self.no_lanes - 1:
            for i, car in enumerate(self.lanes[lane_ind + 1].cars):
                if car.position > my_position:
                    left_front = car.position - my_position
                    if i > 0:
                        left_back = my_position = self.lanes[lane_ind + 1].cars[i - 1].position
                    break
            else:
                if (self.lanes[lane_ind + 1].cars):
                    left_back = my_position - self.lanes[lane_ind + 1].cars[-1].position
        else:
            left_front = 0
            left_back = 0

        # right
        if lane_ind > 0:
            for i, car in enumerate(self.lanes[lane_ind - 1].cars):
                if car.position > my_position:
                    right_front = car.position - my_position
                    if i > 0:
                        right_back = my_position - self.lanes[lane_ind - 1].cars[i - 1].position
                    break
            else:
                if (self.lanes[lane_ind - 1].cars):
                    right_back = my_position - self.lanes[lane_ind - 1].cars[0].position
        else:
            right_front = 0
            right_back = 0

        return front, self.no_lanes, self.speed_limit, left_back, right_back, left_front, right_front, frontSpeed
