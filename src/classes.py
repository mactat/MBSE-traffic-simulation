

class Driver:
    def __init__(self, reaction_time, lane_change_behavior=None, exit_behavior=None, breaking_behavior=None):
        self.reaction_time = reaction_time
        self.lane_change_behavior = lane_change_behavior
        self.exit_behavior = exit_behavior
        self.breaking_behavior = breaking_behavior


class Coms:
    def __init__(self, radius, delay):
        self.range = radius
        self.delay = delay


class Car:
    def __init__(self, initial_speed, number = 0, acc = 0, breaking = 0):
        self.driver = Driver(reaction_time=0)
        # In meters from the start of the highway
        self.position = 0
        self.number = number
        # For now we are asuuming that cars are just a point, has to be changed later
        self.size = 0

        # Setter would be better
        self.lane = 0
        self.acc = acc

        #In m/s
        self.current_speed = initial_speed
        self.desired_speed = initial_speed
        self.breaking = breaking
    
    # Has to be depended on driver's behaviour, dummy for now
    def refresh(self,time_elapsed):
        self.current_speed = self.desired_speed
        self.position = self.position + self.current_speed*time_elapsed

class AutonomousCar(Car):
    def __init__(self):
        pass

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



